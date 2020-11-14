class Pratas:
    def __init__(self, quantidade):
        self._pratas = quantidade

    def acrescentar(self, quantidade):
        self._pratas += quantidade

    def desacrescentar(self, quantidade):
        self._pratas -= quantidade

    def __repr__(self):
        return f"${self._pratas}"

    def __str__(self):
        return f"${self._pratas}"

    def __int__(self):
        return self._pratas
