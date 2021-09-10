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
python hex_stake_importer.py 0x8e7e9DF1fB2d5e1E4a16E71606576720fe3aDA00 America/New_York
```
Arguments are (respectively):
- `address` - ethereum address of the HEX staker
- `timezone name` - timezone used for csv generation. If not provided it will be local timezone. Match it with timezone from CoinTracking account seetings if you are not at home. Possible examples: `US/Pacific`, `Canada/Pacific`, `Europe/Berlin`)
- `exchange name` - name of the exchange staking transactions - default is `HEX Stake`

It will print out stake data in the terminal and generate a csv file with the following columns:
```"Type","Buy","Cur.","Sell","Cur.","Fee","Cur.","Exchange","Group","Comment","Date"```

