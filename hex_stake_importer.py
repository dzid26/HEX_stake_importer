import sys
from web3.main import Web3
from HEX import HEX_Contract
from cointracking import CoinTracking_CSV
from cointracking import add_hex_stake_entries_to_csv

def importer(walletAddress, exchangeName):
    
    hex = HEX_Contract()
    
    print("Wallet address: " + walletAddress)

    stake_count = hex.read_stake_count(walletAddress)
    print("Found " + str(stake_count) + " stakes by directly reading contract function...")
    for index in range(0, stake_count):
        stake = hex.read_stake_by_index(walletAddress, index)
    #     print("Stake data: " + str(stake))
    
    all_stakes_from_events=hex.find_all_address_stakes(walletAddress)
    print("\nFound " + str(len(all_stakes_from_events)) + " stakes in contract events:\n")
    for stake in all_stakes_from_events:
        print(stake)


    ct_csv = CoinTracking_CSV("Cointracking - HEX stakes.csv")
    for stake in all_stakes_from_events:
        add_hex_stake_entries_to_csv(ct_csv, stake, exchangeName)



if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print('Please provide your eth wallet address as argument')
        sys.exit(1)
    walletAddress = Web3.toChecksumAddress(args[0])
    if len(args) > 1:
        exchangeName = args[1]
    else:
        exchangeName = "HEX Stake"
    importer(walletAddress, exchangeName)