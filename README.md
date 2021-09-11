# HEX stake importer to CoinTracking.info
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
```
Windows powershell or VScode terminal:
```
python -m venv .venv 
.venv\Scripts\activate
pip install -r requirements.txt

set WEB3_INFURA_PROJECT_ID=YourProjectID
```
ProjectID can be also added to system or to `activate` script of the virtual environment.

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

### **[Example output](test/Stakes_0x748c8f889Dc2EceBc98FD03d1BdD99dF4B56c8e8_L48.csv)**

## Import
- Backup CoinTracking database before running this script. https://cointracking.info/backup_trades.php
- Import the csv file https://cointracking.info/import/import_csv/
- Verify balances grouped by `Hex Stake`: https://cointracking.info/balance_by_exchange.php