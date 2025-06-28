# exceptions.py

class BibliothequeError(Exception):
    """Classe de base pour toutes les erreurs liées à la bibliothèque."""
    pass


class LivreIndisponibleError(BibliothequeError):
    def __init__(self, message="Le livre demandé est déjà emprunté."):
        super().__init__(message)

class LivreInexistantError(BibliothequeError):
    def __init__(self, message="Ce livre n'existe pas dans la bibliothèque."):
        super().__init__(message)

class MembreInexistantError(BibliothequeError):
    def __init__(self, message="Ce membre n'est pas enregistré."):
        super().__init__(message)

class MembreExistantError(BibliothequeError):
    def __init__(self, message="Ce membre est déjà enregistré."):
        super().__init__(message)

class DejaEmprunteError(BibliothequeError):
    def __init__(self, message="Ce livre est déjà emprunté par ce membre."):
        super().__init__(message)

class QuotaEmpruntDepasseError(BibliothequeError):
    def __init__(self, message="Le quota d'emprunts autorisé est dépassé (maximum 3 livres)."):
        super().__init__(message)
