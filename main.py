from loguru import logger
from utils.func import get_accounts_data, shuffle, sleeping
from utils.gas_bridge import GasZip
from web3 import Web3
from settings import *
import sys
import time
import random

logger.remove()
logger.add("./data/log.txt")
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>")
web3_eth = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth', request_kwargs={'timeout': 60}))


class Worker:

    @staticmethod
    def chek_gas_eth():
        while True:
            try:
                res = int(round(Web3.from_wei(web3_eth.eth.gas_price, 'gwei')))
                logger.info(f'Газ сейчас - {res} gwei\n')
                if res <= MAX_GAS_ETH:
                    break
                else:
                    time.sleep(60)
                    continue
            except Exception as error:
                logger.error(error)
                time.sleep(30)
                continue

    def work(self):
        i = 0
        for number, account in keys_list:
            str_number = f'{number} / {all_wallets}'
            key, proxy = account
            i += 1
            address = web3_eth.eth.account.from_key(key).address
            logger.info(f'Account #{i} || {address}\n')
            zp = GasZip(key, CHAIN_FROM, str_number, proxy)
            number_trans = random.randint(NUMBER_OF_REPETITION[0], NUMBER_OF_REPETITION[1])
            logger.info(f'Number of transactions - {number_trans}\n')
            for _ in range(number_trans):
                self.chek_gas_eth()
                zp.refuel()
                sleeping(TIME_DELAY[0], TIME_DELAY[1])

            logger.success(f'Account completed, sleep and move on to the next one\n')
            sleeping(TIME_ACCOUNT_DELAY[0], TIME_ACCOUNT_DELAY[1])


if __name__ == '__main__':
    list1 = get_accounts_data()
    all_wallets = len(list1)
    logger.info(f'Number of wallets: {all_wallets}\n')
    keys_list = shuffle(list1)

    worker = Worker()
    worker.work()
