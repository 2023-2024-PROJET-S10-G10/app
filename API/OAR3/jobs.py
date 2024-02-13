from API.OAR3.apiclient import ApiClient

class JobAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def jobs(self):
        """
        :return: une liste paginée des jobs selon divers critères tels que l'utilisateur, les dates de début et de fin, les états, et les identifiants des emplois.
        """
        pass

    def job(self, jobId):
        """
        Affiche les détails d'un job spécifique.
        """
        pass

    def nodes(self, jobId):
        """
        :return: les nœuds associés à un job donné.
        """
        pass

    def resource(self, jobId):
        """
        :return: les ressources associées à un job donné.
        """
        pass

    def postJob(self, command, resource, waitList):
        """
        Soumet un nouveau job avec divers paramètres, tels que la commande, les ressources, la file d'attente, etc.
        """
        pass

    def deleteJob(self, jobId):
        """
        Supprime le job spécifié.
        """
        pass

    def signal(self, jobId, signal):
        """
        Envoie un signal au job spécifié.
        """
        pass

    def checkpoint(self, jobId):
        """
        Crée un nouveau point de contrôle pour le job spécifié.
        """
        pass

    def resume(self, jobId):
        """
        Reprend l'exécution d'un job en attente.
        """
        pass

    def hold(self, jobId):
        """
        Place un emploi en attente de manière temporaire.
        """
        pass