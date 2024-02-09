from API.OAR3.apiclient import ApiClientStub
from TestManager import TestManager

class send_requestUT(TestManager):

    def responseValue_returnResponseWithSameValue(self):
        value = b'responseValue'
        apiClientStub = ApiClientStub(response_content=value)

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
