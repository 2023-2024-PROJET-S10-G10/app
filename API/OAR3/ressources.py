from API.OAR3.apiclient import ApiClient

class ResourceAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def resources(self):
        """
        :return: une liste paginée de ressources avec des détails facultatifs, tels que l'adresse réseau.
        """
        pass

    def busyResources(self):
        """
        :return: un dictionnaire indiquant le nombre de ressources occupées.
        """
        pass

    def resource(self, resourceId):
        """
        Affiche les détails d'une ressource spécifique.
        """
        pass

    def jobs(self, resourceId):
        """
        :return: une liste paginée des emplois associés à une ressource donnée.
        """
        pass

    def state(self, resourceId):
        """
        Change l'état d'une ressource et envoie des notifications.
        """
        pass

    def createResource(self, name, properties):
        """
        Crée une nouvelle ressource avec un nom d'hôte et des propriétés spécifiés.
        """
        pass

    def deleteResource(self, resourceId):
        """
        Supprime la ressource spécifiée avec l'identifiant correspondant.
        """
        pass