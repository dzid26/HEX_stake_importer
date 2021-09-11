from cointracking import CoinTracking_CSV
from HEX.hex_api import HEX_Stake
import datetime
from pytz import timezone

IMPORTING_GOOD_ACCOUNTING = False
# IMPORTING_GOOD_ACCOUNTING is set to False because it wouldn't make sense to import stake (income) data to the tax software
# when that option was made exactly to be able to delay the taxable income. It's a bit of a shame though,
# because it would be nicely visible which stakes where unlocked by good accounting before they were withdrawn.

def toLocalTime(timestamp, tz):
    return datetime.datetime.fromtimestamp(timestamp, tz).timetuple()

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

    ofs = 1 #sec: offset for timestamp to improve cointracking sorting

    if not stake.isAutoStake:
        ct_csv.add_deposit_to_csv(toLocalTime(stake.timestampStart+ofs, tz), HEX_Stake.hearts_to_hex(stake.stakedHearts), "HEX", Comment=comment_str + " for " + str(stake.stakedDays) + " days")
    else:
        ct_csv.add_minting_to_csv(toLocalTime(stake.timestampStart, tz), HEX_Stake.hearts_to_hex(stake.stakedHearts), "HEX", Comment="Auto-" + comment_str + " for " + str(stake.stakedDays) + " days")
    if stake.timestampUnlock is not None and stake.timestampUnlock is not stake.timestampEnd and IMPORTING_GOOD_ACCOUNTING:
    #good accounting scenario - use unlock timestamp
        ct_csv.add_staking_to_csv(toLocalTime(stake.timestampUnlock, tz), HEX_Stake.hearts_to_hex(stake.payout), "HEX", Comment=comment_str + " payout")      
        if stake.penalty is not None:
            days_diff = stake.unlockedDay-stake.lockedDay-stake.stakedDays
            ct_csv.add_otherfee_to_csv(toLocalTime(stake.timestampUnlock, tz), HEX_Stake.hearts_to_hex(stake.penalty), "HEX", Comment=comment_str + " penalty " + str(abs(days_diff)) + " days " + ("over" if days_diff > 0 else "early"))
    if stake.timestampEnd is not None and (not stake.prevUnlocked or not IMPORTING_GOOD_ACCOUNTING):
    # or if good accounting wasn't used or good accounting shall be imported when stake ends - then use end timestamp
        ct_csv.add_staking_to_csv(toLocalTime(stake.timestampEnd-ofs, tz), HEX_Stake.hearts_to_hex(stake.payout), "HEX", Comment=comment_str + " payout")      
        if stake.penalty is not None:
            days_diff = stake.unlockedDay-stake.lockedDay-stake.stakedDays
            ct_csv.add_otherfee_to_csv(toLocalTime(stake.timestampEnd-ofs, tz), HEX_Stake.hearts_to_hex(stake.penalty), "HEX", Comment=comment_str + " penalty " + str(abs(days_diff)) + " days " + ("over" if days_diff > 0 else "early"))
    if stake.timestampEnd is not None:    
        ct_csv.add_withdrawal_to_csv(toLocalTime(stake.timestampEnd, tz), HEX_Stake.hearts_to_hex(stake.stakedHearts+stake.payout-stake.penalty), "HEX", Comment=comment_str + " end")
 