from hex_stake_importer import main
from itertools import islice


class TestImporter:
    def test_import_from_blockchain(self):
        ref_lim = 48 # number of transactions to be compared agains reference file (in case this address will have new transactions)
        main(["0x748c8f889Dc2EceBc98FD03d1BdD99dF4B56c8e8", "America/New_York"])
        assert [row for row in islice(open("Cointracking - HEX stakes.csv"), ref_lim)] == [row for row in open("test/Stakes_0x748c8f889Dc2EceBc98FD03d1BdD99dF4B56c8e8_L48.csv")]

        