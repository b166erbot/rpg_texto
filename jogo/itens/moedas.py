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

    def __add__(self, other):
        if isinstance(other, int):
            return self.__class__(self._pratas + other)
        elif isinstance(other, self.__class__):
            return self.__class__(self._pratas + other._pratas)
        else:
            raise TypeError(f"tipo não suportavel {other.__class__}")

    def __radd__(self, other):
        if isinstance(other, int):
            return self.__class__(self._pratas + other)
        elif isinstance(other, self.__class__):
            return self.__class__(self._pratas + other._pratas)
        else:
            raise TypeError(f"tipo não suportavel {other.__class__}")
