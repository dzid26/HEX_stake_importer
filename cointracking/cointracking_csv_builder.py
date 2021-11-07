import csv
import time

COINTRACKING_CSV_HEADER = [ "Type","Buy","Cur.","Sell","Cur.","Fee","Cur.","Exchange","Group","Comment","Date" ]

class _HandlerCSV:
    """
    CoinTracking_CSV class
    """
    def __init__(self, new_csv_file):
        self.csv_table = new_csv_file

    def create_csv(self, data):
        """
        Create csv file from data
        """
        with open(self.csv_table, 'w', newline='') as f: #the example csv had Windows CLRF line endings
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(data)

    def append_csv(self, data):
        """
        Append data to csv file
        """
        with open(self.csv_table, 'a', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(data)

    def remove_trailing(self, new_csv_file):
        """
        Remove trailing line from csv file
        """
        with open(new_csv_file, 'r') as f:
            lines = f.read()
        with open(new_csv_file, 'w') as f:
            f.write(lines[:-1])

class TxType:
    class Trades:
        Trade = "Trade"
        Margin = "Margin Trade"
        Derivatives = "Derivatives / Futures Trade"
    
    class Incoming:
        # General
        Deposit = "Deposit"
        Income = "Income"
        GiftReceive = "Gift / Tip"
        # Blockchain
        Reward = "Reward / Bonus"
        Mining = "Mining"
        Airdrop = "Airdrop"
        Staking = "Staking"
        Masternode = "Masternode"
        Minting = "Minting"
        Mining = "Mining (commercial)"
        # Interests
        Dividends = "Dividends Income"
        Lending = "Lending Income"
        Interest = "Interest Income"
        # Advanced
        Derivatives = "Derivatives / Futures Profit"
        Margin = "Margin Profit"
        Other = "Other Income"
        Income = "Income (non taxable)"

    class Outgoing:
        # General
        Withdrawal = "Withdrawal"
        Spend = "Spend"
        Donation = "Donation"
        GiftGive = "Gift"
        Stolen = "Stolen"
        Lost = "Lost"
        #Interests fees
        Borrowing = "Borrowing Fee"
        Settlement = "Settlement Fee"
        # Advanced
        Margin = "Margin Loss"
        Margin = "Margin Fee"
        Derivatives = "Derivatives / Futures Loss"
        OtherFee = "Other Fee"
        OtherExpense = "Other Expense"
        Expense = "Expense (non taxable)"



class CoinTracking_CSV(_HandlerCSV):
    """
    CoinTracking_CSV class
    """
    def __init__(self, new_csv_file):
        self.csv_table = new_csv_file
        self.handler_csv = _HandlerCSV(self.csv_table)
        self.handler_csv.create_csv(COINTRACKING_CSV_HEADER)
        self.defaultExchange = "Other exchange"
        self.defaultGroup = ""

    def __del__(self):
        self.handler_csv.remove_trailing(self.csv_table)


    @staticmethod
    def dateStr(date):
        """
        Convert entry date to string
        """
        return time.strftime("%Y/%m/%d %H:%M:%S", date)

    def add_entry_to_csv(self, Date:time.struct_time, Type, Buy, BuyCur, Sell, SellCur, Fee="", FeeCur="", Exchange="", Group="", Comment=""):
        """
        Add entry to csv file
        """
        if not Exchange:
            Exchange = self.defaultExchange
        if not Group:
            Group = self.defaultGroup
 
        self.handler_csv.append_csv([[Type, Buy, BuyCur, Sell, SellCur, Fee, FeeCur, Exchange, Group, Comment, self.dateStr(Date)]])

    #generic
    def add_type_trade_to_csv(self, Type, Date:time.struct_time, BuyValue, BuyCur, SellValue, SellCur, Fee="", FeeCur="", Exchange="", Group="", Comment=""):
        """
        Add trade entry to csv file
        """
        self.add_entry_to_csv(Date, Type, BuyValue, BuyCur, SellValue, SellCur, Fee, FeeCur, Exchange, Group, Comment)

    def add_type_incoming_to_csv(self, Date:time.struct_time, Type: TxType.Incoming, Value, Cur, Fee="", FeeCur="", Exchange="", Group="", Comment=""):
        """
        Add incoming entry to csv file
        """
        self.add_entry_to_csv(Date, Type, Value, Cur, "", "", Fee, FeeCur, Exchange, Group, Comment)

    def add_type_outgoing_to_csv(self, Date:time.struct_time, Type: TxType.Outgoing, Value, Cur, Fee="", FeeCur="", Exchange="", Group="", Comment=""):
        """
        Add outgoing entry to csv file
        """
        self.add_entry_to_csv(Date, Type, "", "", Value, Cur, Fee, FeeCur, Exchange, Group, Comment)

    
    #Simple trade
    def add_trade_to_csv(self, Date:time.struct_time, BuyValue, BuyCur, SellValue, SellCur, Fee="", FeeCur="", Exchange="", Group="", Comment=""):
        """
        Add simple trade entry to csv file
        """
        self.add_type_trade_to_csv(Date, TxType.Trades.Trade, BuyValue, BuyCur, SellValue, SellCur, Fee, FeeCur, Exchange, Group, Comment)

    #Simple incoming
    def add_deposit_to_csv(self, Date:time.struct_time, Value, Cur, Fee="", FeeCur="", Exchange="", Group="", Comment=""):
        """
        Add deposit entry to csv file
        """
        self.add_type_incoming_to_csv(Date, TxType.Incoming.Deposit, Value, Cur, Fee, FeeCur, Exchange, Group, Comment)

    def add_staking_to_csv(self, Date:time.struct_time, Value, Cur, Exchange="", Group="", Comment=""):
        """
        Add staking entry to csv file
        """
        self.add_type_incoming_to_csv(Date, TxType.Incoming.Staking, Value, Cur, "", "", Exchange, Group, Comment)
        
    def add_minting_to_csv(self, Date:time.struct_time, Value, Cur, Exchange="", Group="", Comment=""):
        """
        Add minting entry to csv file
        """
        self.add_type_incoming_to_csv(Date, TxType.Incoming.Minting, Value, Cur, "", "", Exchange, Group, Comment)

    #Simple outgoing
    def add_withdrawal_to_csv(self, Date:time.struct_time, Value, Cur, Fee="", FeeCur="", Exchange="", Group="", Comment=""):
        """
        Add withdrawal entry to csv file
        """
        self.add_type_outgoing_to_csv(Date, TxType.Outgoing.Withdrawal, Value, Cur, Fee, FeeCur, Exchange, Group, Comment)
    
    def add_otherfee_to_csv(self, Date:time.struct_time, Value, Cur, Exchange="", Group="", Comment=""):
        """
        Add other fee entry to csv file
        """
        self.add_type_outgoing_to_csv(Date, TxType.Outgoing.OtherFee, Value, Cur, "", "", Exchange, Group, Comment)
