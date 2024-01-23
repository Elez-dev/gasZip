from web3 import Web3
import time
from settings import CHAIN_RPC
from web3.middleware import geth_poa_middleware
from requests.adapters import Retry
import requests
from loguru import logger
from settings import ZORA_GASPRICE_PRESCALE, BASE_GASPRICE_PRESCALE, BSC_GWEI
from utils.chain import *
import random

SCAN = {
    Arbitrum: 'https://arbiscan.io/tx/',
    Optimism: 'https://optimistic.etherscan.io/tx/',
    Polygon: 'https://polygonscan.com/tx/',
    Base: 'https://basescan.org/tx/',
    Zora: 'https://explorer.zora.energy/tx/',
    Nova: 'https://nova.arbiscan.io/tx/',
    BSC: 'https://bscscan.com/tx/',
    Celo: 'https://celoscan.io/tx/',
    Gnosis: 'https://gnosisscan.io/tx/',
    Fantom: 'https://ftmscan.com/tx/',
    Moonriver: 'https://moonriver.moonscan.io/tx/',
    Moonbeam: 'https://moonscan.io/tx/',
    Harmony: 'https://explorer.harmony.one/tx/',
    Linea: 'https://lineascan.build/tx/',
    Scroll: 'https://scrollscan.com/tx/',
    zkEVM: 'https://zkevm.polygonscan.com/tx/',
    Kava: 'https://kavascan.com/tx/',
    Klaytn: 'https://klaytnscope.com/tx/'
}


class Wallet:

    def __init__(self, private_key, chain, number, proxy):
        self.private_key = private_key
        self.chain = chain
        self.number = number
        self.proxy = proxy
        self.web3 = self.get_web3(chain)
        self.scan = self.get_scan(chain)
        self.address_wallet = self.web3.eth.account.from_key(private_key).address

    def get_web3(self, chain):
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        if self.proxy is not None:
            proxy_dick = {'https': 'http://' + self.proxy, 'http': 'http://' + self.proxy}
            session.proxies = proxy_dick
        return Web3(Web3.HTTPProvider(CHAIN_RPC[chain], request_kwargs={'timeout': 60}, session=session))

    @staticmethod
    def get_scan(chain):
        return SCAN[chain]

    @staticmethod
    def to_wei(decimal, amount):
        if decimal == 6:
            unit = 'picoether'
        else:
            unit = 'ether'

        return Web3.to_wei(amount, unit)

    @staticmethod
    def from_wei(decimal, amount):
        if decimal == 6:
            unit = 'picoether'
        elif decimal == 8:
            return float(amount / 10 ** 8)
        else:
            unit = 'ether'

        return Web3.from_wei(amount, unit)

    def send_transaction_and_wait(self, tx, message):
        signed_txn = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info('Sent a transaction')
        time.sleep(5)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=900, poll_latency=5)
        if tx_receipt.status == 1:
            logger.success('The transaction was successfully mined')
        else:
            logger.error("Transaction failed, I'm trying again")
            raise ValueError('')

        logger.success(f'[{self.number}] {message} || {self.scan}{tx_hash.hex()}\n')
        return tx_hash

    def get_native_balance(self):
        return self.web3.eth.get_balance(self.address_wallet)

    def get_gas_price(self):
        if self.chain in ["Polygon", "Avax", 'Zora']:
            try:
                self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            except:
                pass

        if self.chain in [Zora, BSC, Base, Fantom, Core, Moonriver, Moonbeam, Harmony, Scroll, Kava, Klaytn]:
            if self.chain == BSC:
                gwei = round(random.uniform(BSC_GWEI[0], BSC_GWEI[1]), 1)
                return {'gasPrice': Web3.to_wei(gwei, 'gwei')}
            elif self.chain == Zora:
                return {'maxFeePerGas': int(self.web3.eth.gas_price * ZORA_GASPRICE_PRESCALE), 'maxPriorityFeePerGas': int(self.web3.eth.max_priority_fee * ZORA_GASPRICE_PRESCALE)}
            elif self.chain == Base:
                return {'maxFeePerGas': int(self.web3.eth.gas_price * BASE_GASPRICE_PRESCALE), 'maxPriorityFeePerGas': int(self.web3.eth.max_priority_fee * BASE_GASPRICE_PRESCALE)}
            else:
                return {'gasPrice': self.web3.eth.gas_price}
        return {'maxFeePerGas': self.web3.eth.gas_price, 'maxPriorityFeePerGas': self.web3.eth.max_priority_fee}

    @staticmethod
    def get_api_call_data_post(url, json):

        with requests.Session() as s:
            call_data = s.post(url, json=json, timeout=60)
        if call_data.status_code < 400:
            api_data = call_data.json()
            return api_data
        else:
            logger.error("Couldn't get a response")
            raise ValueError('')

    @staticmethod
    def create_data(chain_id_list, value_list):
        data = []
        for i in range(len(chain_id_list)):
            deposit_param = chain_id_list[i] << 240
            value = value_list[i]
            replacement_bytes = value.to_bytes(30, byteorder='big')
            deposit_param_bytes = deposit_param.to_bytes(32, byteorder='big')
            modified_bytes = deposit_param_bytes[:-30] + replacement_bytes
            data.append(int.from_bytes(modified_bytes, byteorder='big'))
        return data

