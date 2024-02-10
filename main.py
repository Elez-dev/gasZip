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

    def __init__(self):
        self.version = None
        self.action = None
        self.chain_lists = {
            1: {
                2: [Gnosis, Fuse, Core, Klaytn, Celo, Harmony, Loot, Moonbeam, Moonriver, opBNB, Viction],
                3: [Fuse, Gnosis, Moonbeam],
                4: [Gnosis, opBNB, Moonbeam, Nova, Zora],
                5: [Fuse, Celo, Moonbeam, Klaytn],
                6: [Gnosis, Moonbeam, Moonriver, opBNB, Fuse, Celo, Harmony],
                7: [Gnosis, Fuse, Core, Moonriver, Viction, Klaytn, Celo, Harmony, Loot, Moonbeam, Nova, opBNB, Moonriver]
            },
            2: {
                2: [Gnosis, Fuse, Core, Klaytn, Celo, Harmony, Loot, Moonbeam, Moonriver, opBNB, Viction],
                3: [Fuse, Gnosis, Viction, Klaytn, Kava, Moonriver, Moonbeam, Loot, Harmony, Core],
                4: [Gnosis, Celo, Fuse, Kava, Klaytn, Harmony, Core, Moonbeam, Moonriver, Viction, Loot],
                5: [Fuse, Celo, Moonbeam, Moonriver, Klaytn, Core, Kava, Harmony, Loot, Viction],
                6: [Gnosis, Moonbeam, Moonriver, opBNB, Fuse, Celo, Harmony, Core, Klaytn, Kava, Loot, Viction],
                7: [Gnosis, Fuse, Core, Moonriver, Viction, Klaytn, Celo, Harmony, Loot, Moonbeam, Nova, opBNB, Moonriver]
            }
        }

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
                    zp.refuel(self.version)
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 2:
                zp = GasZip(key, Polygon, self.chain_lists[self.version][2], str_number, proxy)
                self.chek_gas_eth()
                zp.refuel(self.version)

            if self.action == 3:
                zp = GasZip(key, Celo, self.chain_lists[self.version][3], str_number, proxy)
                self.chek_gas_eth()
                zp.refuel(self.version)

            if self.action == 4:
                zp = GasZip(key, Base, self.chain_lists[self.version][4], str_number, proxy)
                self.chek_gas_eth()
                zp.refuel(self.version)

            if self.action == 5:
                zp = GasZip(key, Gnosis, self.chain_lists[self.version][5], str_number, proxy)
                self.chek_gas_eth()
                zp.refuel(self.version)

            if self.action == 6:
                zp = GasZip(key, Fantom, self.chain_lists[self.version][6], str_number, proxy)
                self.chek_gas_eth()
                zp.refuel(self.version)

            if self.action == 7:
                zp = GasZip(key, Optimism, self.chain_lists[self.version][7], str_number, proxy)
                self.chek_gas_eth()
                zp.refuel(self.version)

            if self.action == 9:
                zp = GasZip(key, CHAIN_FROM, [], str_number, proxy)
                if self.version == 1:
                    zp.check_gas_v1()
                else:
                    zp.check_gas_v2()
                return

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
                            zp.refuel(self.version)
                            sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 2:
                        zp = GasZip(key, Polygon, self.chain_lists[self.version][2], str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel(self.version)
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 3:
                        zp = GasZip(key, Celo, self.chain_lists[self.version][3], str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel(self.version)
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 4:
                        zp = GasZip(key, Base, self.chain_lists[self.version][4], str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel(self.version)
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 5:
                        zp = GasZip(key, Gnosis, self.chain_lists[self.version][5], str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel(self.version)
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 6:
                        zp = GasZip(key, Fantom, self.chain_lists[self.version][6], str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel(self.version)
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

                    if module == 7:
                        zp = GasZip(key, Optimism, self.chain_lists[self.version][7], str_number, proxy)
                        self.chek_gas_eth()
                        zp.refuel(self.version)
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

            logger.success(f'Account completed, sleep and move on to the next one\n')
            sleeping(TIME_ACCOUNT_DELAY[0], TIME_ACCOUNT_DELAY[1])

    def display_menu(self):
        logger.info('''
Select LayerZero version:
1 - LayerZero V1
2 - LayerZero V2
        ''')
        time.sleep(0.1)
        self.version = int(input('Choose a version: '))

    def display_version_menu(self):
        if self.version == 1:
            logger.info('''
1 - Run according to your chosen settings
2 - Polygon  -> Gnosis, Fuse, CoreDAO, Klaytn, Celo, Harmony, Loot, Moonbeam, Moonriver, opBNB, Viction - Fee: $0.74
3 - Celo     -> Fuse, Gnosis, Moonbeam - Fee: $0.16    
4 - Base     -> Gnosis, opBNB, Moonbeam, Nova, Zora - Fee: $0.43
5 - Gnosis   -> Fuse, Celo, Moonbeam, Klaytn - Fee: $0.19  
6 - Fantom   -> Gnosis, Moonbeam, Moonriver, opBNB, Fuse, Celo, Harmony - Fee: $0.40
7 - Optimism -> Gnosis, Fuse, CoreDAO, Moonriver, Viction, Klaytn, Celo, Harmony, Loot, Moonbeam, Nova, opBNB, Moonriver - Fee: $0.68
8 - Mega route: 1 - 7 modules together randomly
9 - Check price
            ''')
        else:
            logger.info('''
1 - Run according to your chosen settings
2 - Polygon  -> Gnosis, Fuse, CoreDAO, Klaytn, Celo, Harmony, Loot, Moonbeam, Moonriver, opBNB, Viction - Fee: $0.67
3 - Celo     -> Fuse, Gnosis, Viction, Klaytn, Kava, Moonriver, Moonbeam, Loot, Harmony, CoreDAO - Fee: $0.55
4 - Base     -> Gnosis, Celo, Fuse, Kava, Klaytn, Harmony, CoreDAO, Moonbeam, Moonriver, Viction, Loot - Fee: $0.56
5 - Gnosis   -> Fuse, Celo, Moonbeam, Moonriver, Klaytn, CoreDAO, Kava, Harmony, Loot, Viction - Fee: $0.49    
6 - Fantom   -> Gnosis, Moonbeam, Moonriver, opBNB, Fuse, Celo, Harmony, CoreDAO, Klaytn, Kava, Loot, Viction - Fee: $0.62
7 - Optimism -> Gnosis, Fuse, CoreDAO, Moonriver, Viction, Klaytn, Celo, Harmony, Loot, Moonbeam, Nova, opBNB, Moonriver - Fee: $0.63
8 - Mega route: 1 - 7 modules together randomly
9 - Check price
                    ''')

        self.action = int(input('Choose an action: '))

    def run(self):
        while True:
            while True:
                self.display_menu()
                if self.version in range(1, 3):
                    break

            while True:
                self.display_version_menu()
                if self.action in range(1, 10):
                    break

            self.work()


if __name__ == '__main__':
    list1 = get_accounts_data()
    all_wallets = len(list1)
    logger.info(f'Number of wallets: {all_wallets}\n')
    keys_list = shuffle(list1)

    worker = Worker()
    worker.run()
