from utils.chain import *

EXCEL_PASSWORD = False  # Если ставите пароль на Excel с приватниками || True/ False
SHUFFLE_WALLETS = True  # Перемешка кошельков                         || True/ False

CHAIN_RPC = {
    Arbitrum : 'https://1rpc.io/arb',
    Optimism : 'https://1rpc.io/op',
    Polygon  : 'https://1rpc.io/matic',
    Zora     : 'https://rpc.zora.energy',  # https://zora.rpc.thirdweb.com
    Base     : 'https://rpc.ankr.com/base',
    Nova     : 'https://rpc.ankr.com/arbitrumnova',
    BSC      : 'https://rpc.ankr.com/bsc',
    Celo     : 'https://rpc.ankr.com/celo',
    Gnosis   : 'https://rpc.ankr.com/gnosis',
    Fantom   : 'https://rpc.ankr.com/fantom',
    Core     : 'https://rpc.ankr.com/core',
    Moonriver: 'https://moonriver.publicnode.com',
    Moonbeam : 'https://rpc.ankr.com/moonbeam',
    Harmony  : 'https://rpc.ankr.com/harmony',
    Linea    : 'https://1rpc.io/linea',
    Scroll   : 'https://rpc.ankr.com/scroll',
    zkEVM    : 'https://rpc.ankr.com/polygon_zkevm',
    Kava     : 'https://rpc.ankr.com/http/kava_api',
    Klaytn   : 'https://rpc.ankr.com/klaytn'
}

MAX_GAS_ETH = 40                 # gas в gwei (смотреть здесь : https://etherscan.io/gastracker)
ZORA_GASPRICE_PRESCALE = 0.0001  # Использовать Max base fee и Priority fee для газа в Zora, экономия 0.3-0.5$
BASE_GASPRICE_PRESCALE = 0.05    # Использовать Max base fee и Priority fee для газа в Base
BSC_GWEI = [1.1, 1.2]

RETRY = 5                        # Количество попыток при ошибках / фейлах
TIME_DELAY = [200, 250]          # Задержка после ТРАНЗАКЦИЙ         [min, max]
TIME_ACCOUNT_DELAY = [20, 30]  # Задержка между АККАУНТАМИ         [min, max]
TIME_DELAY_ERROR = [10, 20]      # Задержка при ошибках / фейлах     [min, max]


VALUE = [0.000005, 0.0000005, 8]          # Количество получаемых токенов [min, max, round_decimal] Общая настройка для всех модулей

# 1 module -----------------------------------------------------------------------------------------------------------------------------------------------------------

CHAIN_FROM = Fantom                        # Из какой сети делать транзы. Доступно || Arbitrum, Optimism, Polygon, Zora,
                                            # Base, Nova, BSC, Celo, Gnosis, Fantom, Core, Moonriver, Moonbeam, Harmony, Linea, Scroll, zkEVM, Kava, Klaytn

CHAIN_DEP = [Moonbeam]            # Сюда пишем сети которые полюбому будут
CHAIN_DEP_RANDOM = []         # Сюда пишем сети которые будут рандомно
# Доступные сети
# Polygon, Arbitrum, Optimism, BSC, Avax, Base, Gnosis, Core, Celo, Moonriver, Fantom, Kava, Linea, Moonbeam, Harmony,
# Canto, Mantle, Nova, Fuse, Beam, Metis, Astar, Conflux, Horizen, Klaytn, Loot, Manta, Meter, OKX, opBNB, Orderly,
# PGN, zkEVM, Scroll, Telos, Tenet, Viction, XPLA, Zora

NUMBER_OF_REPETITION = [1, 2]               # количество транз [min, max]

# 8 module -----------------------------------------------------------------------------------------------------------------------------------------------

MODULE = [1, 2, 3, 4, 5, 6, 7]
