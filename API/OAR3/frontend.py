from API.OAR3.apiclient import ApiClient

class FrontendAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def oarVersion(self):
        """
        :return: les versions de l'API et d'OAR.
        """
        return self.client.get("/")

    def versions(self):
        """
        :return: les versions d'OAR, de l'API et des librairies associées.
        """
        return self.client.get("/version")

    def whoAmI(self):
        """
        :return: le nom de l'utilisateur authentifié.
        """
        return self.client.get("/whoami")

    def checkToken(self):
        """
        Vérifie la validité du jeton d'authentification.
        """
        return self.client.get("/check_token")

    def timeZone(self):
        """
        :return: le fuseau horaire du serveur API OAR.
        """
        return self.client.get("/timezone")

    def checkAuthentification(self):
        """
        Vérifie si les informations d'authentification de base sont valides.
        """
        return self.client.get("/authentication")
