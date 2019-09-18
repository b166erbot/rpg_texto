class PocaoDeCura:
    def __init__(self, pontos_cura: int, quantidade: int):
        self.pontos_cura = pontos_cura
        self.quantidade = quantidade

    def repr(self):
        return (f"{self.nome.captalize()}: {self.quantidade} - "
                f"Cura: {self.pontos_cura}")

    def __bool__(self):
        return bool(self.quantidade)

    def __iadd__(self, other):
        if isinstance(other, self.__class__):
            self.quantidade += other.quantidade
            return self
        else:
            texto = 'tipo de operando não suportado entre: {} e {}'
            raise TypeError(texto.format(type(self), type(other)))

    def consumir(self):
        if self.quantidade > 0:
            self.quantidade -= 1
            return self.pontos_cura
        return 0


class PocaoDeVidaFraca(PocaoDeCura):
    nome = 'poção de vida fraca'
    custo = 15
    def __init__(self, quantidade: int = 1):
        super().__init__(30, quantidade)

class PocaoDeVidaMedia(PocaoDeCura):
    nome = 'poção de vida média'
    custo = 30
    def __init__(self, quantidade: int = 1):
        super().__init__(60, quantidade)

class PocaoDeVidaGrande(PocaoDeCura):
    nome = 'poção de vida grande'
    custo = 45
    def __init__(self, quantidade: int = 1):
        super().__init__(90, quantidade)

class PocaoDeVidaExtraGrande(PocaoDeCura):
    nome = 'poção de vida extra grande'
    custo = 60
    def __init__(self, quantidade: int = 1):
        super().__init__(120, quantidade)

# elixir deve regenerar porcentagem de vida. implementar isso futuramente.
class ElixirDeVidaFraca(PocaoDeCura):
    nome = 'elixir de vida fraca'
    custo = 100
    def __init__(self, quantidade: int = 1):
        super().__init__(150, quantidade)

class ElixirDeVidaMedia(PocaoDeCura):
    nome = 'elixir de vida média'
    custo = 200
    def __init__(self, quantidade: int = 1):
        super().__init__(180, quantidade)

class ElixirDeVidaGrande(PocaoDeCura):
    nome = 'elixir de vida grande'
    custo = 300
    def __init__(self, quantidade: int = 1):
        super().__init__(210, quantidade)

class ElixirDeVidaExtraGrande(PocaoDeCura):
    nome = 'elixir de vida extra grande'
    custo = 400
    def __init__(self, quantidade: int = 1):
        super().__init__(240, quantidade)


curas = [
    PocaoDeVidaFraca, PocaoDeVidaMedia, PocaoDeVidaGrande,
    PocaoDeVidaExtraGrande, ElixirDeVidaFraca, ElixirDeVidaMedia,
    ElixirDeVidaGrande, ElixirDeVidaExtraGrande
]
