from jogo.tela.imprimir import formas


class Moedas:
    def __init__(self, nome: str, quantidade: int):
        self._nome = nome
        self._moedas = quantidade

    def __repr__(self):
        return f"{self._nome}: ${self._moedas}"

    def __str__(self):
        return f"{self._nome}: ${self._moedas}"

    def __int__(self):
        return self._moedas

    def __add__(self, other):
        if isinstance(other, int):
            return self.__class__(self._moedas + other)
        elif isinstance(other, self.__class__):
            return self.__class__(self._moedas + other._moedas)
        else:
            raise TypeError(f"tipo não suportavel {other.__class__}")

    def __radd__(self, other):
        if isinstance(other, int):
            return self.__class__(self._moedas + other)
        elif isinstance(other, self.__class__):
            return self.__class__(self._moedas + other._moedas)
        else:
            raise TypeError(f"tipo não suportavel {other.__class__}")

    def __sub__(self, other):
        if isinstance(other, int):
            return self.__class__(self._moedas - other)
        elif isinstance(other, self.__class__):
            return self.__class__(self._moedas - other._moedas)
        else:
            raise TypeError(f"tipo não suportavel {other.__class__}")

    def __rsub__(self, other):
        if isinstance(other, int):
            return self.__class__(self._moedas - other)
        elif isinstance(other, self.__class__):
            return self.__class__(self._moedas - other._moedas)
        else:
            raise TypeError(f"tipo não suportavel {other.__class__}")


class Pratas(Moedas):
    def __init__(self, quantidade: int):
        super().__init__('Pratas', quantidade)


class Draconica(Moedas):
    def __init__(self, quantidade: int):
        super().__init__('Draconica', quantidade)
    
    def __repr__(self):
        return f"{self._nome}: {formas[148]} {self._moedas}"

    def __str__(self):
        return f"{self._nome}: {formas[148]} {self._moedas}"
