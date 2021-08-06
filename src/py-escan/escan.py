from dotenv import load_dotenv
from dotmap import DotMap
import requests
import os


class Etherscan:
    load_dotenv()
    ETHERS_TOKEN = os.getenv('ETHERSCAN_TOKEN')

    def __init__(self):
        self.key = self.ETHERS_TOKEN
        self.url = 'https://api.etherscan.io/api?'

    def _query(self, module, params: DotMap):

        query = f'module={module}'
        for key, value in params.items():
            query += f'&{key}={value}'

        url = f'{self.url}{query}&apikey={self.key}'

        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            r = r.json()
        except requests.exceptions.RequestException as err:
            return err
        else:
            if r['status'] == '1':
                return r['result']

    def get_birth_block(self, address):
        module = 'account'
        params = DotMap()
        params.action = 'txlist'
        params.address = address
        params.startblock = '0'
        params.endblock = '99999999'
        params.order = 'asc'
        response = self._query(module, params)
        if response is not None:
            return int(response[0]['blockNumber'])
        else:
            return None

    def get_txns(self, address):
        module = 'account'
        params = DotMap()
        first_block = self.get_birth_block(address)

        if first_block is None:
            first_block = 0

        params.action = 'txlist'
        params.sort = 'desc'
        params.startblock = str(first_block)
        params.endblock = 'latest'
        params.address = str(address).lower()
        return self._query(module, params)

    def get_tokentxns(self, address):
        module = 'account'
        params = DotMap()
        first_block = self.get_birth_block(address)

        if first_block is None:
            first_block = 0

        params.action = 'tokentx'
        params.sort = 'desc'
        params.startblock = str(first_block)
        params.endblock = 'latest'
        params.address = str(address).lower()
        return self._query(module, params)

    def get_events(self, contract, event):
        module = 'logs'
        params = DotMap()
        first_block = self.get_birth_block(contract)
        params.action = 'getLogs'
        params.fromBlock = str(first_block)
        params.toBlock = 'latest'
        params.address = contract
        params.topic0 = event
        return self._query(module, params)

    def get_block_countdown(self, block):
        module = 'block'
        params = DotMap()
        params.action = 'getblockcountdown'
        params.blockno = block
        response = self._query(module, params)
        return response['EstimateTimeInSec']
