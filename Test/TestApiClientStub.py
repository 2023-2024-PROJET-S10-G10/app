from API.OAR3.apiclient import ApiClientStub
from TestManager import TestManager

class send_requestUT(TestManager):

    def responseValue_returnResponseWithSameValue(self):
        value = b'responseValue'
        apiClientStub = ApiClientStub(body=value)

        response = apiClientStub.send_request('GET').read()

        self.assertEqual(response, value)

    def responseStatus_returnResponseWithSameStatus(self):
        status = 200
        apiClientStub = ApiClientStub(status=status)

        response = apiClientStub.send_request('get').status

        self.assertEqual(response, status)

    def responseHeaders_returnResponseWithSameHeaders(self):
        headers = {
            'Content-Type': 'application/json',
            'test': 'test'
        }
        apiClientStub = ApiClientStub(headers=headers)

        response = apiClientStub.send_request('get').headers

        self.assertEqual(response, headers)

    def mockMultipleURL_ReturnEachAssiociatedResponse(self):
        apiClientStub = ApiClientStub()
        value1 = b'response1'
        value2 = b'response2'
        value3 = b'response3'

        apiClientStub.mock('get', 'test1', body=value1)
        apiClientStub.mock('get', 'test2', body=value2)
        apiClientStub.mock('get', 'test3', body=value3)
        response1 = apiClientStub.send_request(method='get', url='test1')
        response2 = apiClientStub.send_request(method='get', url='test2')
        response3 = apiClientStub.send_request(method='get', url='test3')

        self.assertEqual(response1.read(), value1)
        self.assertEqual(response2.read(), value2)
        self.assertEqual(response3.read(), value3)
