from API.OAR3.apiclient import ApiClient


class JobAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def jobs(self, user=None, start_time=None, stop_time=None, states=None, array=None, job_ids=None, details=None,
             offset=0, limit=500):
        """
        :return: une liste paginée des jobs selon divers critères tels que l'utilisateur, les dates de début et de fin, les états, et les identifiants des emplois.
        """
        args = locals().copy()
        args.pop("self")
        args = {k: v for k, v in args.items() if v is not None}
        return self.client.get("/jobs" + ApiClient.queries(**args))

    def job(self, jobId, details: bool = False):
        """
        Affiche les détails d'un job spécifique.
        """
        return self.client.get("/jobs/" + str(jobId) + ApiClient.queries(details=details))

    def nodes(self, jobId, limit=500, offset=0):
        """
        :return: les nœuds associés à un job donné.
        """
        return self.client.get("/jobs/" + str(jobId) + "/nodes" + ApiClient.queries(limit=limit, offset=offset))

    def resource(self, jobId, limit=500, offset=0):
        """
        :return: les ressources associées à un job donné.
        """
        return self.client.get("/jobs/" + str(jobId) + "/nodes" + ApiClient.queries(limit=limit, offset=offset))

    def postJob(self, body):
        """
        Soumet un nouveau job avec divers paramètres, tels que la commande, les ressources, la file d'attente, etc.
        """
        return self.client.post('/jobs', body=body)

    def deleteJob(self, jobId, array: bool = False):
        """
        Supprime le job spécifié.
        """
        return self.client.delete('/jobs/' + str(jobId) + ApiClient.queries(array='true' if array else 'false'))

    def signal(self, jobId, signal):
        """
        Envoie un signal au job spécifié.
        """
        return self.client.post('/jobs/' + str(jobId) + '/signal/' + str(signal))

    def checkpoint(self, jobId):
        """
        Crée un nouveau point de contrôle pour le job spécifié.
        """
        return self.client.post('/jobs/' + str(jobId) + '/checkpoint/new')

    def resume(self, jobId):
        """
        Reprend l'exécution d'un job en attente.
        """
        return self.client.post('/jobs/' + str(jobId) + '/resumptions/new')

    def hold(self, jobId, hold):
        """
        Place un emploi en attente de manière temporaire.
        """
        return self.client.post('/jobs/' + str(jobId) + hold)
