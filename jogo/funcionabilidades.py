class Contador:
    def __init__(self, contagem_maxima: int):
        self._contagem_maxima = contagem_maxima
        self._contagem = 0

    def acrescentar(self):
        self._contagem += 1

    def resetar(self):
        self._contagem = 0

    @property
    def usar(self):
        return True if self._contagem > self._contagem_maxima else False
