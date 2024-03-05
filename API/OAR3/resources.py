from API.apiclient import ApiClient


class ResourceAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def resources(
        self, offset=None, limit=None, detailed=None, network_address=None
    ):
        """
        :return: une liste paginée de ressources avec des détails facultatifs, tels que l'adresse réseau.
        """
        args = locals().copy()
        args.pop("self")
        args = {k: v for k, v in args.items() if v is not None}
        return self.client.get("/resources" + ApiClient.queries(**args))

    def busyResources(self):
        """
        :return: un dictionnaire indiquant le nombre de ressources occupées.
        """
        return self.client.get("/resources/busy")

    def resource(self, resourceId):
        """
        Affiche les détails d'une ressource spécifique.
        """
        pass

    def jobs(self, resourceId, limit=None, offset=None):
        """
        :return: une liste paginée des emplois associés à une ressource donnée.
        """
        args = locals().copy()
        args.pop("self")
        args.pop("resourceId")
        args = {k: v for k, v in args.items() if v is not None}
        return self.client.get(
            "/resources/"
            + str(resourceId)
            + "/jobs"
            + ApiClient.queries(**args)
        )

    def state(self, resourceId, body={}):
        """
        Change l'état d'une ressource et envoie des notifications.
        """
        return self.client.post(
            "/resources/" + str(resourceId) + "/state", body=body
        )

    def createResource(self, hostname, properties):
        """
        Crée une nouvelle ressource avec un nom d'hôte et des propriétés spécifiés.
        """
        return self.client.post(
            "/resources"
            + ApiClient.queries(hostname=hostname, properties=properties)
        )

    def deleteResource(self, resourceId):
        """
        Supprime la ressource spécifiée avec l'identifiant correspondant.
        """
        return self.client.delete("/resources/" + str(resourceId))
