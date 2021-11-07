#pytest

import time
from cointracking import CoinTracking_CSV

CSV_REF = """\
"Type","Buy","Cur.","Sell","Cur.","Fee","Cur.","Exchange","Group","Comment","Date"
"Deposit","4","USD","","","","","Other exchange","","","1970/01/01 00:00:00"
"Withdrawal","","","4","USD","","","Other exchange","","","1970/01/01 00:00:00"
"Staking","4","USD","","","","","Other exchange","","","1970/01/01 00:00:00"
"Other Fee","","","4","USD","","","Other exchange","","","1970/01/01 00:00:00"\
"""

class TestCsvExport():
    def test_csv_export(self):
        test_file = "test_export.csv"
        ct_csv = CoinTracking_CSV(test_file)
        ct_csv.add_deposit_to_csv(time.localtime(0), 4, "USD")
        ct_csv.add_withdrawal_to_csv(time.localtime(0), 4, "USD")
        ct_csv.add_staking_to_csv(time.localtime(0), 4, "USD")
        ct_csv.add_otherfee_to_csv(time.localtime(0), 4, "USD")
        
        assert  [row.rstrip('\n') for row in open(test_file)] == [row for row in CSV_REF.split("\n")]
