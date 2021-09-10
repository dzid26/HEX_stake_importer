from cointracking import CoinTracking_CSV
from HEX.hex_api import HEX_Stake
import datetime
from pytz import timezone


def add_hex_stake_entries_to_csv(ct_csv: CoinTracking_CSV, stake: HEX_Stake, exchange="Hex Stake", group="", timezone_name=None):
    """
    Add stake entries to csv file. No tx fees for stake entries. Comments include Stake ID.
    :param ct_csv: CoinTracking_CSV object
    :param stake: HEX_Stake object
    :param Exchange: Exchange name
    :param Group: Trading Group name
    :param timezone: timezone offset in hours - negative for USA, positive for Europe
    """
    ct_csv.defaultExchange = exchange
    ct_csv.defaultGroup = group
    if timezone_name:
        tz = timezone(timezone_name)
    else:
        tz = None #local system timezone

    comment_str = "Stake #" + str(stake.stakeId)
    local_time_start = datetime.datetime.fromtimestamp(stake.timestampStart, tz).timetuple()
    
    ct_csv.add_deposit_to_csv(local_time_start, HEX_Stake.hearts_to_hex(stake.stakedHearts), "HEX", Comment=comment_str)
    if stake.timestampEnd is not None:
        local_time_end = datetime.datetime.fromtimestamp(stake.timestampEnd, tz).timetuple()
        
        ct_csv.add_staking_to_csv(local_time_end, HEX_Stake.hearts_to_hex(stake.payout), "HEX", Comment=comment_str)
        ct_csv.add_withdrawal_to_csv(local_time_end, HEX_Stake.hearts_to_hex(stake.stakedHearts), "HEX", Comment=comment_str)
        if stake.penalty is not None:
            ct_csv.add_otherfee_to_csv(local_time_end, HEX_Stake.hearts_to_hex(stake.penalty), "HEX", Comment=comment_str)