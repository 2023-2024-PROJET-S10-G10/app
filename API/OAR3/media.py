from API.OAR3.apiclient import ApiClient

class MediaAPI:
    def __init__(self, client: ApiClient = None):
        if client is None:
            self.client = ApiClient()
        else:
            self.client = client

    def ls(self, path):
        """
        Liste les fichiers dans le dossier spécifié dans le chemin. Les résultats sont paginés et basé sur la limite et l'offset des paramètres de recherche.
        """

        pass

    def getMedia(self, path, textToAdd):
        """
        Récupère le contenu d'un fichier spécifié par le chemin donné en paramètre. Il est possible ajouter du texte en spécifiant le paramètre tail.
        """
        pass

    def postMedia(self, directoryPath, force=False):
        """
        Upload un fichier spécifié par le champ file form. Le paramètre de recherche "force" peut être utilisé pour overwrite des fichiers existants
        """
        pass

    def chmod(self, path, perm):
        """
        Change les permissions d'un fichier spécifié par le paramètre path_filename.
        """
        pass

    def deleteMedia(self, path):
        """
        Supprime le fichier spécifié par le paramètre path_filename.
        """
        pass
