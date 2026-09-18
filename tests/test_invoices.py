import unittest
from typing import get_args
from unittest.mock import Mock

from workbench import InvoiceStatus, InvoiceWriteStatus
from workbench.resources.invoices import InvoicesResource


class InvoiceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.invoices = InvoicesResource(self.client)

    def test_payment_states_rejected_without_http(self):
        for status in ('paid', 'partial', 'voided', 'refunded'):
            with self.subTest(status=status):
                with self.assertRaisesRegex(ValueError, 'read-only'):
                    self.invoices.create(items=[], status=status)
                with self.assertRaisesRegex(ValueError, 'read-only'):
                    self.invoices.update('invoice-id', status=status)
        self.client.post.assert_not_called()
        self.client.put.assert_not_called()

    def test_all_writable_states_preserved(self):
        self.assertEqual(set(get_args(InvoiceWriteStatus)), {'draft', 'sent', 'viewed', 'overdue', 'cancelled'})
        for status in get_args(InvoiceWriteStatus):
            self.invoices.create(items=[], status=status)
            self.client.post.assert_called_with('/v1/invoices', json={'items': [], 'status': status})
            self.invoices.update('invoice-id', status=status, notes='fixture')
            self.client.put.assert_called_with('/v1/invoices/invoice-id', json={'notes': 'fixture', 'status': status})

    def test_payment_filters_remain_readable(self):
        self.assertIn('paid', get_args(InvoiceStatus))
        self.invoices.list(status='paid')
        self.assertEqual(self.client.get.call_args.kwargs['params']['status'], 'paid')

    def test_omitted_status_and_conflict_preserved(self):
        self.invoices.update('invoice-id', notes='fixture')
        self.client.put.assert_called_with('/v1/invoices/invoice-id', json={'notes': 'fixture'})
        self.client.put.side_effect = RuntimeError('Invoice changed. Reload it before retrying.')
        with self.assertRaisesRegex(RuntimeError, 'Reload'):
            self.invoices.update('invoice-id', notes='fixture')


if __name__ == '__main__':
    unittest.main()
