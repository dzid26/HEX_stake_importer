import sys
import json
from web3.main import Web3
from web3.auto.infura import w3


HEX_CONTRACT_ADDRESS = '0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39'
with open('HEX/abi.json') as json_data:
    ABI = json.load(json_data)

class HEX_contract:
    def __init__(self):
        self.hex_ = w3.eth.contract(HEX_CONTRACT_ADDRESS, abi=ABI)
        print("ERC20 contract found:" + self.hex_.functions.name().call() + " (" + self.hex_.address + ")")

    def get_stake_count(self, walletAddress):
        """
        Get the stake count of an address
        """
        return self.hex_.functions.stakeCount(walletAddress).call()

    def get_stake_data(self, walletAddress, index):
        """
        Get the stake data for an index from an address
        """
        return self.hex_.functions.stakeLists(walletAddress, index).call()


def main():
    """
    Main function
    """
    args = sys.argv[1:]
    if not args:
        print('Please provide your eth wallet address as argument')
        sys.exit(1)
    else:
        address = Web3.toChecksumAddress(args[0])
    hex_ = HEX_contract()

    stake_count = hex_.get_stake_count(address)
    print("Stake count: " + str(stake_count))
    for index in range(0, stake_count):
        stake_data = hex_.get_stake_data(address, index)
        print("Stake data: " + str(stake_data))


if __name__ == "__main__":
    main()