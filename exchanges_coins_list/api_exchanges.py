import requests
from logger import logger
from db_manager import DBManager

BINANCE_ENDPOINT = 'https://api.binance.com/api/v3/exchangeInfo'
COINBASE_ENDPOINT = 'https://api.coinbase.com/v2/currencies/crypto'
BYBIT_ENDPOINT = 'https://api-testnet.bybit.com/spot/v3/public/symbols'
KUCOIN_ENDPOINT = 'https://api.kucoin.com/api/v1/market/allTickers'

class APIRequest:
    def __init__(self):
        self.db_manager = DBManager()
        self.logger = logger

    async def make_request(self, api_url: str) -> dict:
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            json_data = response.json()

            endpoint_mapping = {
                BINANCE_ENDPOINT: self.process_binance_endpoint,
                COINBASE_ENDPOINT: self.process_coinbase_endpoint,
                BYBIT_ENDPOINT: self.process_bybit_endpoint,
                KUCOIN_ENDPOINT: self.process_kucoin_endpoint
            }

            processing_function = endpoint_mapping.get(api_url)

            if processing_function:
                self.logger.logger.info(f"Processing data from {api_url}")
                processed_data = await processing_function(json_data)  # Await the coroutine
                return processed_data
            else:
                raise ValueError("Unknown API endpoint")

        except requests.exceptions.RequestException as e:
            self.logger.logger.error(f"Error making API request: {e}")
            return None

    async def process_binance_endpoint(self, json_data: dict) -> dict:
        symbols = []
        for item in json_data['symbols']:
            if item['quoteAsset'] in ['USDT', 'BUSD']:
                symbol = {
                    'symbol'    : item['symbol'],
                    'status'    : item['status'],
                    'quoteAsset': item['quoteAsset'],
                    'baseAsset' : item['baseAsset'],
                }
                symbols.append(symbol)
        await self.db_manager.insert_binance_data(symbols)
        return symbols

    async def process_coinbase_endpoint(self, json_data: dict) -> dict:
        symbols = []
        for item in json_data['data']:
            symbol = {
                'code'      : item['code'],
                'asset_id'  : item['asset_id'],
            }
            symbols.append(symbol)
        
        await self.db_manager.insert_coinbase_data(symbols)
        return symbols
    
    async def process_bybit_endpoint(self, json_data: dict) -> dict:
        symbols = []
        for item in json_data['result']['list']:
            symbol = {
                'name'      : item['name'],
                'alias'     : item['alias'],
                'baseCoin'  : item['baseCoin'],
                'quoteCoin' : item['quoteCoin'],
                'showStatus': item['showStatus'],
            }
            symbols.append(symbol)
        await self.db_manager.insert_bybit_data(symbols)
        return symbols
    
    async def process_kucoin_endpoint(self, json_data: dict) -> dict:
        symbols = []
        for item in json_data['data']['ticker']:
            symbol = {
                'symbol': item['symbol']
            }
            symbols.append(symbol)
        await self.db_manager.insert_kucoin_data(symbols)
        return symbols

async def main():
    api_request = APIRequest()
    await api_request.make_request(BINANCE_ENDPOINT)
    await api_request.make_request(COINBASE_ENDPOINT)
    await api_request.make_request(BYBIT_ENDPOINT)
    await api_request.make_request(KUCOIN_ENDPOINT)