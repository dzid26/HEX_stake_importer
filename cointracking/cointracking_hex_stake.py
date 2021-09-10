from cointracking import CoinTracking_CSV
from HEX.hex_api import HEX_Stake
import time


def add_hex_stake_entries_to_csv(ct_csv: CoinTracking_CSV, stake: HEX_Stake, Exchange="Hex Stake", Group=""):
    """
    Add stake entries to csv file. No tx fees for stake entries. Comments include Stake ID.
    :param ct_csv: CoinTracking_CSV object
    :param stake: HEX_Stake object
    :param Exchange: Exchange name
    :param Group: Trading Group name
    """
    ct_csv.defaultExchange = Exchange
    ct_csv.defaultGroup = Group

    comment_str = "Stake #" + str(stake.stakeId)

    ct_csv.add_deposit_to_csv(time.gmtime(stake.timestampStart), HEX_Stake.hearts_to_hex(stake.stakedHearts), "HEX", Comment=comment_str)
    if stake.timestampEnd is not None:
        ct_csv.add_staking_to_csv(time.gmtime(stake.timestampEnd), HEX_Stake.hearts_to_hex(stake.payout), "HEX", Comment=comment_str)
        ct_csv.add_withdrawal_to_csv(time.gmtime(stake.timestampEnd), HEX_Stake.hearts_to_hex(stake.stakedHearts), "HEX", Comment=comment_str)
        if stake.penalty is not None:
            ct_csv.add_otherfee_to_csv(time.gmtime(stake.timestampEnd), HEX_Stake.hearts_to_hex(stake.penalty), "HEX", Comment=comment_str)