from API.OAR3.apiclient import ApiClient

class StressFactorAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def stressFactor(self, script):
        """
        :return: Le facteur de stress en utilisant un script spécifié dans le fichier de configuration. Il est retourné en tant que paire clé-valeur dans un dictionnaire.
        """
        pass
