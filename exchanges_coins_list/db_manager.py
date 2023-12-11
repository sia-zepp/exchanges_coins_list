import sqlite3
from datetime import datetime
from logger import logger
from telegram_bot import TelegramBot

class DBManager:
    def __init__(self):
        self.db_connection = sqlite3.connect('database.db')
        self.db_cursor = self.db_connection.cursor()
        self.logger = logger
        self.bot = TelegramBot()

    def create_tables(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS BINANCE_DATA 
                               (ID INTEGER PRIMARY KEY, 
                               SYMBOL TEXT, 
                               STATUS TEXT, 
                               QUOTE_ASSET TEXT, 
                               BASE_ASSET TEXT, 
                               DATE_TIME TEXT)""")
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS COINBASE_DATA 
                               (ID INTEGER PRIMARY KEY, 
                                CODE TEXT, 
                                ASSET_ID TEXT, 
                                DATE_TIME TEXT)""")
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS BYBIT_DATA 
                               (ID INTEGER PRIMARY KEY, 
                                NAME TEXT, 
                                ALIAS TEXT, 
                                BASE_COIN TEXT, 
                                QUOTE_COIN TEXT, 
                                STATUS TEXT, 
                                DATE_TIME TEXT)""")
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS KUCOIN_DATA 
                               (ID INTEGER PRIMARY KEY, 
                                SYMBOL TEXT, 
                                DATE_TIME TEXT)""")
        self.db_connection.commit()

    async def insert_binance_data(self, symbols: dict):
        self.create_tables()
        for item in symbols:
            symbol      = item['symbol']
            status      = item['status']
            quote_asset = item['quoteAsset']
            base_asset  = item['baseAsset']
            date_time   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.db_cursor.execute("SELECT * FROM BINANCE_DATA WHERE SYMBOL = ?", (symbol,))
            if not self.db_cursor.fetchone():
                self.db_cursor.execute("""INSERT INTO BINANCE_DATA (
                                        SYMBOL, 
                                        STATUS, 
                                        QUOTE_ASSET, 
                                        BASE_ASSET, 
                                        DATE_TIME)
                                        VALUES (?, ?, ?, ?, ?)""", 
                                        (symbol, status, quote_asset, base_asset, date_time))
                self.logger.logger.info(f"Inserted binance data: Symbol={symbol}, Status={status}, Quote Asset={quote_asset}, Base Asset={base_asset}, Date Time={date_time}")
                await self.bot.send_message(f"""🔥BINANCE🔥\n[PAIR] {symbol}\n[DATE] {date_time}\n[WEBSITE] https://www.binance.com""")
        self.db_connection.commit()

    async def insert_coinbase_data(self, symbols: dict):
        self.create_tables()
        for item in symbols:
            code        = item['code']
            asset_id    = item['asset_id']
            date_time   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.db_cursor.execute("SELECT * FROM COINBASE_DATA WHERE CODE = ?", (code,))
            if not self.db_cursor.fetchone():
                self.db_cursor.execute("""INSERT INTO COINBASE_DATA (
                                       CODE, 
                                       ASSET_ID, 
                                       DATE_TIME) 
                                       VALUES (?, ?, ?)""", 
                                       (code, asset_id, date_time))
                self.logger.logger.info(f"Inserted coinbase data: Code={code}, Asset ID={asset_id}, Date Time={date_time}")
                await self.bot.send_message(f"""💧CONIBASE💧\n[COIN] {code}\n[DATE] {date_time}\n[WEBSITE] https://www.coinbase.com/""")
        self.db_connection.commit()

    async def insert_bybit_data(self, symbols: dict):
        self.create_tables()
        for item in symbols:
            name        = item['name']
            alias       = item['alias']
            base_coin   = item['baseCoin']
            quote_coin  = item['quoteCoin']
            status      = item['showStatus']
            date_time   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.db_cursor.execute("SELECT * FROM BYBIT_DATA WHERE NAME = ?", (name,))
            if not self.db_cursor.fetchone():
                self.db_cursor.execute("""INSERT INTO BYBIT_DATA (
                                       NAME, 
                                       ALIAS, 
                                       BASE_COIN, 
                                       QUOTE_COIN, 
                                       STATUS, 
                                       DATE_TIME) 
                                       VALUES (?, ?, ?, ?, ?, ?)""", 
                                       (name, alias, base_coin, quote_coin, status, date_time))
                self.logger.logger.info(f"Inserted bybit data: Name={name}, Alias={alias}, Base Coin={alias}, Quote Coin={base_coin}, Status={status}, Date Time={date_time}")
                await self.bot.send_message(f"""🗿BYBIT🗿\n[PAIR] {name}\n[DATE] {date_time} \n[WEBSITE] https://www.bybit.com/""")
        self.db_connection.commit()

    async def insert_kucoin_data(self, symbols: dict):
        self.create_tables()
        for item in symbols:
            symbol      = item['symbol']
            date_time   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.db_cursor.execute("SELECT * FROM KUCOIN_DATA WHERE SYMBOL = ?", (symbol,))
            if not self.db_cursor.fetchone():
                self.db_cursor.execute("""INSERT INTO KUCOIN_DATA (
                                       SYMBOL, 
                                       DATE_TIME) 
                                       VALUES (?, ?)""", 
                                       (symbol, date_time))
                self.logger.logger.info(f"Inserted bybit data: Name={symbol} Date Time={date_time}")
                await self.bot.send_message(f"""🚸KUCOIN🚸\n[PAIR] {symbol}\n[DATE] {date_time} \n[WEBSITE] https://www.kucoin.com/""")
        self.db_connection.commit()
              
    def __del__(self):
        self.db_cursor.close()
        self.db_connection.close()