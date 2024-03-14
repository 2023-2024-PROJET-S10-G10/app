from API.apiclient import ApiClientStub
from TestManager import TestManager


class send_requestUT(TestManager):
    def responseValue_returnResponseWithSameValue(self):
        value = b"responseValue"
        apiClientStub = ApiClientStub(body=value)

        _, response = apiClientStub.send_request("GET")

        self.assertEqual(response, value)

    def responseStatus_returnResponseWithSameStatus(self):
        status = 200
        apiClientStub = ApiClientStub(status=status)

        response, _ = apiClientStub.send_request("get")

        self.assertEqual(response.status, status)

    def responseHeaders_returnResponseWithSameHeaders(self):
        headers = {"Content-Type": "application/json", "test": "test"}
        apiClientStub = ApiClientStub(headers=headers)

        response, _ = apiClientStub.send_request("get")

        self.assertEqual(response.headers, headers)

    def mockMultipleURL_ReturnEachAssiociatedResponse(self):
        apiClientStub = ApiClientStub()
        value1 = b"response1"
        value2 = b"response2"
        value3 = b"response3"

        apiClientStub.mock("get", "test1", body=value1)
        apiClientStub.mock("get", "test2", body=value2)
        apiClientStub.mock("get", "test3", body=value3)
        _, response1 = apiClientStub.send_request(method="get", url="test1")
        _, response2 = apiClientStub.send_request(method="get", url="test2")
        _, response3 = apiClientStub.send_request(method="get", url="test3")

        self.assertEqual(response1, value1)
        self.assertEqual(response2, value2)
        self.assertEqual(response3, value3)
