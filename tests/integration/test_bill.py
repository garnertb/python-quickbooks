import os
import unittest
from datetime import datetime

from quickbooks.client import QuickBooks
from quickbooks.objects.base import Ref
from quickbooks.objects.bill import Bill, BillLine, AccountBasedExpenseLineDetail
from quickbooks.objects.vendor import Vendor


class BillTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_create(self):
        bill = Bill()

        line = BillLine()
        line.Amount = 200
        line.DetailType = "AccountBasedExpenseLineDetail"

        account_ref = Ref()
        account_ref.type = "Account"
        account_ref.value = 1
        line.AccountBasedExpenseLineDetail = AccountBasedExpenseLineDetail()
        line.AccountBasedExpenseLineDetail.AccountRef = account_ref
        bill.Line.append(line)

        vendor = Vendor.all(max_results=1, qb=self.qb_client)[0]
        bill.VendorRef = vendor.to_ref()

        bill.save(qb=self.qb_client)

        query_bill = Bill.get(bill.Id, qb=self.qb_client)

        self.assertEquals(query_bill.Id, bill.Id)
        self.assertEquals(len(query_bill.Line), 1)
        self.assertEquals(query_bill.Line[0].Amount, 200.0)
