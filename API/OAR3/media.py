from API.OAR3.apiclient import ApiClient


class MediaAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def ls(self, path, limit, offset):
        """
        Liste les fichiers dans le dossier spécifié dans le chemin. Les résultats sont paginés et basé sur la limite et l'offset des paramètres de recherche.
        """

        return self.client.get("/media/ls/" + path + ApiClient.queries(limit=limit, offset=offset))

    def getMedia(self, path, tail):
        """
        Récupère le contenu d'un fichier spécifié par le chemin donné en paramètre. Il est possible ajouter du texte en spécifiant le paramètre tail.
        """
        return self.client.get("/media" + ApiClient.queries(path=path, tail=tail))

    def postMedia(self, fileName, force=False):
        """
        Upload un fichier spécifié par le champ file form. Le paramètre de recherche "force" peut être utilisé pour overwrite des fichiers existants
        """
        with open(fileName, mode='rb') as file:
            return self.client.post("/media" + ApiClient.queries(force=force), body=file.read())

    def deleteMedia(self, path):
        """
        Supprime le fichier spécifié par le paramètre path_filename.
        """
        return self.client.delete("/media" + ApiClient.queries(path=path))

    def chmod(self, path, mode):
        """
        Change les permissions d'un fichier spécifié par le paramètre path_filename.
        """
        return self.client.post("/media/chmod" + ApiClient.queries(path=path, mode=mode))
