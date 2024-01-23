from utils.wallet import Wallet
from loguru import logger
import json as js
from web3 import Web3
from settings import VALUE, CHAIN_DEP, CHAIN_DEP_RANDOM
import random
from utils.retry import exception_handler
from utils.func import lz_id_chain


class GasZip(Wallet):

    def __init__(self, private_key, chain, number, proxy):
        super().__init__(private_key, chain, number, proxy)
        self.abi = js.load(open('./abi/gas.txt'))
        self.contract = self.web3.eth.contract(address=Web3.to_checksum_address('0xBf94Ed69281709958c8f60bc15cD1bB6BADCd4A4'), abi=self.abi)

    @staticmethod
    def add_random_elements():
        random.shuffle(CHAIN_DEP)
        random.shuffle(CHAIN_DEP_RANDOM)
        chain_dep = CHAIN_DEP.copy()
        chain_dep_random = CHAIN_DEP_RANDOM
        num_elements_to_add = random.randint(0, len(chain_dep_random))
        if num_elements_to_add == 0:
            return chain_dep
        random_elements = random.sample(chain_dep_random, num_elements_to_add)
        chain_dep.extend(random_elements)
        return chain_dep

    @staticmethod
    def dst_chain_id_list(mass):
        chain_id_list = [lz_id_chain[chain] for chain in mass]
        return chain_id_list

    @staticmethod
    def native_amount_list(mass):
        native_amount_list = [Web3.to_wei(round(random.uniform(VALUE[0], VALUE[1]), VALUE[2]), 'ether') for _ in mass]
        return native_amount_list

    @exception_handler
    def refuel(self):
        chain_list = self.add_random_elements()
        logger.info(f'Bridge from {self.chain} to {chain_list}')
        id_list = self.dst_chain_id_list(chain_list)
        amount_list = self.native_amount_list(chain_list)
        adapter_params = [self.contract.functions.createAdapterParams(id_list[i], amount_list[i], self.address_wallet).call() for i in range(len(chain_list))]
        fees = sum(self.contract.functions.estimateFees(id_list, adapter_params).call())
        deposit_param = self.create_data(id_list, amount_list)
        dick = {
            "from": self.address_wallet,
            "value": fees,
            "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
            ** self.get_gas_price()
        }
        txn = self.contract.functions.deposit(deposit_param, self.address_wallet).build_transaction(dick)
        self.send_transaction_and_wait(txn, f'Bridge Gas.zip from {self.chain} to {len(chain_list)} chain')