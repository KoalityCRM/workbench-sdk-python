import unittest
from unittest.mock import Mock
import json
import time
from workbench.webhooks import compute_signature, construct_webhook_event, WebhookVerificationError
import httpx
from workbench.client import WorkbenchClient, WorkbenchError
from workbench.resources.integrations import IntegrationsResource
from workbench.resources.clients import ClientsResource
from workbench.resources.invoices import InvoicesResource
from workbench.resources.quotes import QuotesResource


class ContractParityTests(unittest.TestCase):
    def test_integrations_use_real_http_client_and_json_body(self):
        requests = []
        def handle(request):
            requests.append(request)
            return httpx.Response(200, json={'data': {'id': 'integration'}})
        client = WorkbenchClient(api_key='wbk_test_fixture', max_retries=0)
        client._http.close()
        client._http = httpx.Client(base_url='https://fixture.invalid', transport=httpx.MockTransport(handle))
        try:
            resource = IntegrationsResource(client)
            resource.list(page=2)
            resource.get('id')
            resource.get_reviews('id', min_rating=3)
            resource.list_installed()
            resource.get_installed('id')
            resource.install('id', ['clients:read'], 'code', 'verifier')
            resource.disable('id')
            resource.enable('id')
            resource.submit_review('id', 5, title='Good')
            resource.uninstall('id')
            self.assertEqual([r.method for r in requests], ['GET'] * 5 + ['POST'] * 4 + ['DELETE'])
            self.assertEqual(requests[0].url.params['page'], '2')
            self.assertEqual(json.loads(requests[5].content)['authorization_code'], 'code')
            self.assertEqual(json.loads(requests[8].content), {'rating': 5, 'title': 'Good'})
        finally:
            client.close()

    def test_signed_webhook_requires_an_object(self):
        secret = 'fixture-signing-secret'
        timestamp = int(time.time())
        for payload in ['[]', 'null', '"scalar"']:
            signature = compute_signature(payload, secret, timestamp)
            with self.assertRaisesRegex(WebhookVerificationError, 'expected a JSON object'):
                construct_webhook_event(payload, f't={timestamp},v1={signature}', secret)
        payload = '{"event":"invoice.created"}'
        signature = compute_signature(payload, secret, timestamp)
        self.assertEqual(construct_webhook_event(payload, f't={timestamp},v1={signature}', secret)['event'], 'invoice.created')

    def test_non_object_api_response_is_rejected(self):
        client = WorkbenchClient(api_key='wbk_test_fixture', max_retries=0)
        client._http.close()
        client._http = httpx.Client(base_url='https://fixture.invalid', transport=httpx.MockTransport(lambda request: httpx.Response(200, json=[])))
        try:
            with self.assertRaisesRegex(WorkbenchError, 'expected a JSON object'):
                client.get('/v1/clients')
        finally:
            client.close()

    def test_client_lead_stage_and_internal_notes(self):
        client = Mock()
        resource = ClientsResource(client)
        resource.list(lead_status='qualified')
        self.assertEqual(client.get.call_args.kwargs['params']['lead_status'], 'qualified')
        resource.create(first_name='Ada', lead_status='qualified', internal_notes='Fixture')
        client.post.assert_called_once_with('/v1/clients', json={'first_name': 'Ada', 'lead_status': 'qualified', 'internal_notes': 'Fixture'})

    def test_explicit_null_updates_reach_api(self):
        for resource, path in [(ClientsResource, 'clients'), (InvoicesResource, 'invoices'), (QuotesResource, 'quotes')]:
            with self.subTest(resource=path):
                client = Mock()
                resource(client).update('id', notes=None)
                client.put.assert_called_once_with(f'/v1/{path}/id', json={'notes': None})

    def test_discount_and_item_tax_are_preserved(self):
        for resource, path in [(InvoicesResource, 'invoices'), (QuotesResource, 'quotes')]:
            with self.subTest(resource=path):
                client = Mock()
                items = [{'description': 'Service', 'quantity': 1, 'unit_price': 10, 'taxable': False, 'tax_rate': None}]
                resource(client).create(items=items, discount_type='percentage', discount_amount=10)
                client.post.assert_called_once_with(f'/v1/{path}', json={'items': items, 'discount_type': 'percentage', 'discount_amount': 10})

    def test_send_returns_actual_document_response(self):
        for resource, path in [(InvoicesResource, 'invoices'), (QuotesResource, 'quotes')]:
            client = Mock()
            response = {'data': {'id': 'id', 'status': 'sent'}}
            client.post.return_value = response
            self.assertIs(resource(client).send('id'), response)
            client.post.assert_called_once_with(f'/v1/{path}/id/send')


if __name__ == '__main__':
    unittest.main()
