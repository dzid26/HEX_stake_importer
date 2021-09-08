import sys
import time
import json
from web3.main import Web3
from web3.auto.infura import w3


HEX_CONTRACT_ADDRESS = '0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39'
with open('HEX/abi.json') as json_data:
    ABI = json.load(json_data)

DAYS_TO_SECONDS=24*60*60
SECONDS_TO_DAYS=1/DAYS_TO_SECONDS

HEX_LAUNCH_TIME=1575331200
HEARTS_TO_HEX = 1e-8
SHARES_TO_TSHARES = 1e-12


class HEX_Stake:
    def __init__(self, stakeId):
        self.stakeId = stakeId
        self.timestampStart = None
        self.stakedHearts = None
        self.stakeShares = None
        self.lockedDay = None
        self.stakedDays = None
        self.isAutoStake = None
        self.unlockedDay = None
        self.payout = None


    def __str__(self):
        return "Stake ID: " + str(self.stakeId) + "\n" + \
            "Stake submitted: " + (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.timestampStart)) if self.timestampStart else "0-0-0 0:0:0") + "\n" + \
            "Staked Hex: " + str(self.stakedHearts*HEARTS_TO_HEX) + "\n" + \
            ("Interests HEX: " + str(self.payout*HEARTS_TO_HEX) + "\n" if self.payout else "" ) + \
            "Staked TShares: " + str(self.stakeShares*SHARES_TO_TSHARES) + "\n" + \
            "Staked Days: " + str(self.stakedDays) + "\n" + \
            "Locked Day: " + str(self.lockedDay) + "\n" + \
            "Unlocked Day: " + str(self.unlockedDay) + "\n" + \
            "Is Auto Stake: " + str(self.isAutoStake) + "\n"

    
    def processStakeStartData(self, stakeData0):
        # https://etherscan.io/address/0x2b591e99afe9f32eaa6214f7b7629768c40eeb39#code#L571
        # StakeStart        (auto-generated event):
        #     uint40            timestamp       -->  data0 [ 39:  0]
        #     address  indexed  stakerAddr
        #     uint40   indexed  stakeId
        #     uint72            stakedHearts    -->  data0 [111: 40]
        #     uint72            stakeShares     -->  data0 [183:112]
        #     uint16            stakedDays      -->  data0 [199:184]
        #     bool              isAutoStake     -->  data0 [207:200]
        self.timestampStart = stakeData0 & (2**40-1)
        self.stakedHearts = (stakeData0 >> 40) & (2**72-1)
        self.stakeShares = (stakeData0 >> 112) & (2**72-1)
        self.stakedDays = (stakeData0 >> 184) & (2**16-1)
        self.isAutoStake = (stakeData0 >> 200) & (2**1-1)
        self.lockedDay = round((self.timestampStart - HEX_LAUNCH_TIME) * SECONDS_TO_DAYS + .5)+1 #since HEX launch, day 0 is day 1, stake is assumed to start at the end of day


    def processStakeEndData(self, stakeData0, stakeData1):
        # https://etherscan.io/address/0x2b591e99afe9f32eaa6214f7b7629768c40eeb39#code#L571
        # StakeEnd          (auto-generated event)
        #     uint40            timestamp       -->  data0 [ 39:  0]
        #     address  indexed  stakerAddr
        #     uint40   indexed  stakeId
        #     uint72            stakedHearts    -->  data0 [111: 40]
        #     uint72            stakeShares     -->  data0 [183:112]
        #     uint72            payout          -->  data0 [255:184]
        #     uint72            penalty         -->  data1 [ 71:  0]
        #     uint16            servedDays      -->  data1 [ 87: 72]
        #     bool              prevUnlocked    -->  data1 [ 95: 88]

        self.timestampEnd = stakeData0 & (2**40-1)
        self.stakedHearts = (stakeData0 >> 40) & (2**72-1)
        self.stakeShares = (stakeData0 >> 112) & (2**72-1)
        self.payout = (stakeData0 >> 184) & (2**72-1)
        self.penalty = (stakeData1 >> 256) & (2**72-1)
        self.servedDays = (stakeData1 >> 72) & (2**16-1)
        self.prevUnlocked = (stakeData1 >> 88) & (2**1-1)
        self.unlockedDay = round((self.timestampEnd - HEX_LAUNCH_TIME) * SECONDS_TO_DAYS + .5)+1 #since HEX launch, day 0 is day 1, stake is assumed to start at the end of day

class HEX_contract:
    def __init__(self):
        self.hex_ = w3.eth.contract(HEX_CONTRACT_ADDRESS, abi=ABI)
        print("ERC20 contract found:" + self.hex_.functions.name().call() + " (" + self.hex_.address + ")")

    def read_stake_count(self, walletAddress):
        """
        Get the stake count of an address
        """
        return self.hex_.functions.stakeCount(walletAddress).call()

    def read_stake_by_index(self, walletAddress, index): 
        """
        Get the stake data for an index from an address
        """
        stakeId, stakedHearts, stakeShares, lockedDay, stakedDays, unlockedDay, isAutoStake \
            = self.hex_.functions.stakeLists(walletAddress, index).call()
        staked_HEX = stakedHearts*HEARTS_TO_HEX
        stakedTShares = stakeShares*SHARES_TO_TSHARES
        lockedDate = time.gmtime(HEX_LAUNCH_TIME + stakedDays*DAYS_TO_SECONDS)
        
        stake = HEX_Stake(stakeId)
        stake.stakedHearts = staked_HEX
        stake.stakeShares = stakedTShares
        stake.lockedDay = lockedDay
        stake.stakedDays = stakedDays
        stake.unlockedDay = unlockedDay
        stake.isAutoStake = isAutoStake
        return stake

    def find_all_address_stakes(self, address):
        """
        Find the stake data for an address
        """
        stakeStartedEventsForAddress=self.hex_.events.StakeStart.createFilter(fromBlock=0, argument_filters={'stakerAddr': address}).get_all_entries()
        
        all_stakes = []
        for event in stakeStartedEventsForAddress:
            stakeId = event['args']['stakeId']
            stakeData0 = event['args']['data0']
            stake = HEX_Stake(stakeId)
            stake.processStakeStartData(stakeData0)

            stakeEndedEventsForAddress=self.hex_.events.StakeEnd.createFilter(fromBlock=0, argument_filters={'stakerAddr': address}).get_all_entries()
            for event in stakeEndedEventsForAddress:
                if event['args']['stakeId'] == stakeId:
                    stakeData0 = event['args']['data0']
                    stakeData1 = event['args']['data1']
                    stake.processStakeEndData(stakeData0, stakeData1)
                    break

            all_stakes.append(stake)
        return all_stakes




        

def main():
    """
    Main function
    """

    args = sys.argv[1:]
    if not args:
        print('Please provide your eth wallet address as argument')
        sys.exit(1)
    else:
        walletAddress = Web3.toChecksumAddress(args[0])
    hex = HEX_contract()
    
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


if __name__ == "__main__":
    main()