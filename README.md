# HEX stake importer
To import staking data in readable format and saves as csv that can be imported by cointracking.info. It complements normal Ethereum blockchain import.


## Prerequisites

- Install Python 3.9
- Get Infura API key
- Install packages. You can use virtual pipenv environment, e.g:

Linux:
```
python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt

export WEB3_INFURA_PROJECT_ID=YourProjectID
export WEB3_INFURA_API_SECRET=YourProjectSecret
```
Windows:
```
python -m venv .venv 
.venv\Scripts\activate
pip install -r requirements.txt

set WEB3_INFURA_PROJECT_ID=YourProjectID
set WEB3_INFURA_API_SECRET=YourProjectSecret
```

## Usage:
Example with using some long term staker address:
```
python hex_stake_importer.py 0x748c8f889Dc2EceBc98FD03d1BdD99dF4B56c8e8 America/New_York
```
Arguments are (respectively):
- `address` - ethereum address of the HEX staker
- `timezone name` - timezone used for csv generation. If not provided it will be local timezone. Match it with timezone from CoinTracking account seetings if you are not at home. Possible examples: `US/Pacific`, `Canada/Pacific`, `Europe/Berlin`)
- `exchange name` - name of the exchange staking transactions - default is `HEX Stake`

It will print out stake data in the terminal and generate a csv file with the following columns:
```"Type","Buy","Cur.","Sell","Cur.","Fee","Cur.","Exchange","Group","Comment","Date"```

Example output:
```
"Minting","4812.25730085","HEX","","","","","HEX Stake","","Auto-Stake #24342 for 3650 days","2019/12/04 20:06:33"
"Deposit","534.695","HEX","","","","","HEX Stake","","Stake #24422 for 3650 days","2019/12/04 20:15:28"
"Staking","0.0","HEX","","","","","HEX Stake","","Stake #24422 payout","2019/12/06 00:13:51"
"Other Fee","","","248.406298","HEX","","","HEX Stake","","Stake #24422 penalty 3649 days early","2019/12/06 00:13:51"
"Withdrawal","","","286.288702","HEX","","","HEX Stake","","Stake #24422 end","2019/12/06 00:13:51"
"Deposit","224257.0","HEX","","","","","HEX Stake","","Stake #29993 for 100 days","2019/12/05 19:55:57"
"Staking","3313.56975266","HEX","","","","","HEX Stake","","Stake #29993 payout","2020/03/18 13:00:59"
"Other Fee","","","0.0","HEX","","","HEX Stake","","Stake #29993 penalty 3 days over","2020/03/18 13:00:59"
"Withdrawal","","","227570.56975266","HEX","","","HEX Stake","","Stake #29993 end","2020/03/18 13:00:59"
"Deposit","289960.0","HEX","","","","","HEX Stake","","Stake #33362 for 348 days","2019/12/06 19:03:33"
"Staking","9135.03805006","HEX","","","","","HEX Stake","","Stake #33362 payout","2020/05/10 18:21:28"
"Other Fee","","","10321.40662798","HEX","","","HEX Stake","","Stake #33362 penalty 193 days early","2020/05/10 18:21:28"
```

## Import
- Backup CoinTracking database before running this script. https://cointracking.info/backup_trades.php
- Import the csv file https://cointracking.info/import/import_csv/
- Verify balances grouped by `Hex Stake`: https://cointracking.info/balance_by_exchange.php