from API.OAR3.apiclient import ApiClient


class ProxyAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def proxy(self, jobId):
        """
        Redirige vers l'URL cible définie pour le travail spécifié en utilisant Traefik comme proxy.
        """
        self.client.get("/proxy/" + jobId)
