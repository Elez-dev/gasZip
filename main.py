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

    def __init__(self, action):
        super().__init__()
        self.action = action

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

            if self.action == 1:
                chain_list = self.add_random_elements()
                zp = GasZip(key, CHAIN_FROM, chain_list, str_number, proxy)
                number_trans = random.randint(NUMBER_OF_REPETITION[0], NUMBER_OF_REPETITION[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    self.chek_gas_eth()
                    zp.refuel()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 2:
                chain_list = [Gnosis, Fuse, Core, Kava, Klaytn, Celo, Harmony, Loot, Moonbeam, Moonriver, Astar,
                              Viction, Beam]
                zp = GasZip(key, Polygon, chain_list, str_number, proxy)
                self.chek_gas_eth()
                zp.refuel()

            if self.action == 3:
                chain_list = [Fuse, Gnosis, Moonbeam]
                zp = GasZip(key, Celo, chain_list, str_number, proxy)
                self.chek_gas_eth()
                zp.refuel()

            if self.action == 4:
                chain_list = [Gnosis, opBNB, Moonbeam, Nova, Zora]
                zp = GasZip(key, Base, chain_list, str_number, proxy)
                self.chek_gas_eth()
                zp.refuel()

            if self.action == 5:
                chain_list = [Fuse, Celo, Moonbeam, Klaytn]
                zp = GasZip(key, Gnosis, chain_list, str_number, proxy)
                self.chek_gas_eth()
                zp.refuel()

            if self.action == 6:
                chain_list = [Gnosis, Moonbeam, Moonriver, opBNB, Kava, Beam, Celo, Harmony]
                zp = GasZip(key, Fantom, chain_list, str_number, proxy)
                self.chek_gas_eth()
                zp.refuel()

            if self.action == 7:
                chain_list = [Kava, Gnosis, Fuse, Core, Moonriver, Viction, Beam, Klaytn, Celo, Harmony, Loot, Moonbeam]
                zp = GasZip(key, Optimism, chain_list, str_number, proxy)
                self.chek_gas_eth()
                zp.refuel()

            if self.action == 8:
                random.shuffle(MODULE)
                for module in MODULE:
                    if module == 1:
                        chain_list = self.add_random_elements()
                        zp = GasZip(key, CHAIN_FROM, chain_list, str_number, proxy)
                        number_trans = random.randint(NUMBER_OF_REPETITION[0], NUMBER_OF_REPETITION[1])
                        logger.info(f'Number of transactions - {number_trans}\n')
                        for _ in range(number_trans):
                            self.chek_gas_eth()
                            zp.refuel()
                            sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 2:
                        chain_list = [Gnosis, Fuse, Core, Kava, Klaytn, Celo, Harmony, Loot, Moonbeam, Moonriver, Astar,
                                      Viction, Beam]
                        zp = GasZip(key, Polygon, chain_list, str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel()
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 3:
                        chain_list = [Fuse, Gnosis, Moonbeam]
                        zp = GasZip(key, Celo, chain_list, str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel()
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 4:
                        chain_list = [Gnosis, opBNB, Moonbeam, Nova, Zora]
                        zp = GasZip(key, Base, chain_list, str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel()
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 5:
                        chain_list = [Fuse, Gnosis, Moonbeam, Klaytn]
                        zp = GasZip(key, Gnosis, chain_list, str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel()
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 6:
                        chain_list = [Gnosis, Moonbeam, Moonriver, opBNB, Kava, Beam, Celo, Harmony]
                        zp = GasZip(key, Fantom, chain_list, str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel()
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 7:
                        chain_list = [Kava, Gnosis, Fuse, Core, Moonriver, Viction, Beam, Klaytn, Celo, Harmony, Loot,
                                      Moonbeam]
                        zp = GasZip(key, Optimism, chain_list, str_number, proxy)
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

    while True:
        while True:
            logger.info('''
1 - Run according to your chosen settings
2 - Polygon  -> Gnosis, Fuse, CoreDAO, Kava, Klaytn, Celo, Harmony, Loot, Moonbeam, Moonriver, Astar, Viction, Beam - LayerZero Fee: $0.73
3 - Celo     -> Fuse, Gnosis, Moonbeam - LayerZero Fee: $0.15     
4 - Base     -> Gnosis, opBNB, Moonbeam, Nova, Zora - LayerZero Fee: $0.41  
5 - Gnosis   -> Fuse, Celo, Moonbeam, Klaytn - LayerZero Fee: $0.18     
6 - Fantom   -> Gnosis, Moonbeam, Moonriver, opBNB, Kava, Beam, Celo, Harmony - LayerZero Fee: $0.47
7 - Optimism -> Kava, Gnosis, Fuse, CoreDAO, Moonriver, Viction, Beam, Klaytn, Celo, Harmony, Loot, Moonbeam - LayerZero Fee: $0.57
8 - Mega route: 1 - 7 modules together randomly
            ''')

            time.sleep(0.1)
            act = int(input('Choose an action: '))

            if act in range(1, 9):
                break

        worker = Worker(act)
        worker.work()
