import http.client
import io
import json


class ApiClient:
    _instance = None
    _headers = {}

    def __init__(self, host="", port="", baseEndpoint="", headers={}):
        self.client = http.client.HTTPConnection(
            host, port
        )  # context=ssl._create_unverified_context()) # à utiliser si problème de https
        self._headers = self._headers | headers
        self.baseEndpoint = baseEndpoint

    def set_host(self, host, port):
        self.client.host = host
        self.client.port = port

    def send_request(self, method, url, headers={}, body={}):
        self.client.request(
            method,
            self.baseEndpoint + url,
            headers=headers | self._headers,
            body=json.dumps(body),
        )
        res = self.client.getresponse()
        content = res.read()
        self.client.close()
        return res, content

    @staticmethod
    def queries(**queries):
        if len(queries) == 0:
            return ""
        query_string = "?"
        for elt in queries:
            if type(queries[elt]) is list:
                for value in queries[elt]:
                    query_string += str(elt) + "=" + str(value) + "&"
            else:
                query_string += str(elt) + "=" + str(queries[elt]) + "&"
        return query_string[0:-1]

    def get(self, url, headers={}, body={}):
        """
        Do a GET request
        :param url: request url
        :param headers: dict of headers
        :param body: dict of body's elements
        """
        return self.send_request("GET", url, headers, body)

    def delete(self, url, headers={}, body={}):
        """
        Do a DELETE request
        :param url: request url
        :param headers: dict of headers
        :param body: dict of body's elements
        """
        return self.send_request("DELETE", url, headers, body)

    def post(self, url, headers={}, body={}):
        """
        Do a POST request
        :param url: request url
        :param headers: dict of headers
        :param body: dict of body's elements
        """
        return self.send_request("POST", url, headers, body)


class ApiClientStub(ApiClient):
    class SocketStub(io.BytesIO):
        def makefile(self, _):
            pass

    def __init__(
        self,
        body=b"<html><body><h1>404 Error</h1></body></html>",
        status=404,
        headers={},
    ):
        response = {"content": body, "status": status, "headers": headers}
        self.mockedValue = {"getdefault": response}

    def mock(self, method, url, status=200, headers={}, body=b""):
        self.mockedValue[method.lower() + url] = {
            "content": body,
            "status": status,
            "headers": headers,
        }

    def send_request(self, method, url="getdefault", headers={}, body={}):
        response = self.mockedValue.get(
            method.lower() + url, self.mockedValue["getdefault"]
        )
        conn = http.client.HTTPConnection("getdefault")

        simulated_response = http.client.HTTPResponse(
            ApiClientStub.SocketStub(response["content"])
        )
        simulated_response.chunked = False
        simulated_response.length = None
        simulated_response.status = response["status"]
        simulated_response.headers = response["headers"]

        conn.close()

        return simulated_response, response["content"]
