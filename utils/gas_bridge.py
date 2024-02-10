import time

from utils.wallet import Wallet
from loguru import logger
import json as js
from web3 import Web3
from settings import VALUE
import random
from utils.retry import exception_handler
from utils.func import lz_id_chain


class GasZip(Wallet):

    def __init__(self, private_key, chain, chain_list, number, proxy):
        super().__init__(private_key, chain, number, proxy)
        self.chain_list = chain_list
        self.abi_v1 = js.load(open('./abi/gas_v1.txt'))
        self.abi_v2 = js.load(open('./abi/gas_v2.txt'))
        self.contract_v1 = self.web3.eth.contract(address=Web3.to_checksum_address('0xBf94Ed69281709958c8f60bc15cD1bB6BADCd4A4'), abi=self.abi_v1)
        self.contract_v2 = self.web3.eth.contract(address=Web3.to_checksum_address('0x26da582889f59eaae9da1f063be0140cd93e6a4f'), abi=self.abi_v2)

    @staticmethod
    def dst_chain_id_list(mass):
        chain_id_list = [lz_id_chain[chain] for chain in mass]
        return chain_id_list

    @staticmethod
    def native_amount_list(mass):
        native_amount_list = [Web3.to_wei(round(random.uniform(VALUE[0], VALUE[1]), VALUE[2]), 'ether') for _ in mass]
        return native_amount_list

    @staticmethod
    def create_data_v1(chain_id_list, value_list):
        data = []
        for i in range(len(chain_id_list)):
            deposit_param = chain_id_list[i] << 240
            value = value_list[i]
            replacement_bytes = value.to_bytes(30, byteorder='big')
            deposit_param_bytes = deposit_param.to_bytes(32, byteorder='big')
            modified_bytes = deposit_param_bytes[:-30] + replacement_bytes
            data.append(int.from_bytes(modified_bytes, byteorder='big'))
        return data

    @staticmethod
    def create_data_v2(chain_id_list, value_list):
        data = []
        for i in range(len(chain_id_list)):
            deposit_param = chain_id_list[i] << 224
            value = value_list[i]
            mask = (1 << 128) - 1
            modified_bytes = (deposit_param & ~mask) | (value & mask)
            data.append(modified_bytes)
        return data

    def check_gas_v1(self):
        for name, _id in lz_id_chain.items():
            amount_list = self.native_amount_list([_id])
            adapter_params = [self.contract_v1.functions.createAdapterParams([_id][i], amount_list[i], self.address_wallet).call() for i in range(len([_id]))]
            try:
                fees = Web3.from_wei(sum(self.contract_v1.functions.estimateFees([_id], adapter_params).call()), 'ether')
            except:
                fees = None
            logger.info(f'Bridge from {self.chain} to {name} || {fees}')
            time.sleep(0.1)

    @exception_handler
    def refuel_v1(self):
        logger.info(f'Bridge from {self.chain} to {self.chain_list}')
        id_list = self.dst_chain_id_list(self.chain_list)
        amount_list = self.native_amount_list(self.chain_list)
        adapter_params = [self.contract_v1.functions.createAdapterParams(id_list[i], amount_list[i], self.address_wallet).call() for i in range(len(self.chain_list))]
        fees = sum(self.contract_v1.functions.estimateFees(id_list, adapter_params).call())
        deposit_param = self.create_data_v1(id_list, amount_list)
        dick = {
            "from": self.address_wallet,
            "value": fees,
            "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
            ** self.get_gas_price()
        }
        txn = self.contract_v1.functions.deposit(deposit_param, self.address_wallet).build_transaction(dick)
        self.send_transaction_and_wait(txn, f'Bridge Gas.zip from {self.chain} to {len(self.chain_list)} chain')

    def check_gas_v2(self):
        for name, _id in lz_id_chain.items():
            _id += 30000
            amount_list = self.native_amount_list([_id])
            adapter_params = [self.contract_v2.functions.createNativeDropOption([_id][i], amount_list[i], self.address_wallet).call() for i in range(len([_id]))]
            try:
                fees = Web3.from_wei(sum(self.contract_v2.functions.estimateFees([_id], ['0x' for _ in range(len([_id]))], adapter_params).call()), 'ether')
            except:
                fees = None
            logger.info(f'Bridge from {self.chain} to {name} || {fees}')
            time.sleep(0.1)

    @exception_handler
    def refuel_v2(self):
        logger.info(f'Bridge from {self.chain} to {self.chain_list}')
        id_list = [ids + 30000 for ids in self.dst_chain_id_list(self.chain_list)]
        amount_list = self.native_amount_list(self.chain_list)
        adapter_params = [self.contract_v2.functions.createNativeDropOption(id_list[i], amount_list[i], self.address_wallet).call() for i in range(len(self.chain_list))]
        fees = sum(self.contract_v2.functions.estimateFees(id_list, ['0x' for _ in range(len([id_list]))], adapter_params).call())
        deposit_param = self.create_data_v2(id_list, amount_list)
        dick = {
            "from": self.address_wallet,
            "value": fees,
            "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
            ** self.get_gas_price()
        }
        txn = self.contract_v2.functions.sendDeposits(deposit_param, self.address_wallet).build_transaction(dick)
        self.send_transaction_and_wait(txn, f'Bridge Gas.zip from {self.chain} to {len(self.chain_list)} chain')

    def refuel(self, version):
        if version == 1:
            self.refuel_v1()
        else:
            self.refuel_v2()
