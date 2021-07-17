class PocaoDeCura:
    def __init__(self, pontos_cura: int):
        self.pontos_cura = pontos_cura
        self.consumida = False
        self.preco = self.custo

    def __repr__(self):
        return (f"{self.nome.capitalize()} - "
                f"Cura: {self.pontos_cura}")

    def consumir(self):
        if not self.consumida:
            self.consumida = True
            return self.pontos_cura
        return 0


class PocaoDeVidaFraca(PocaoDeCura):
    nome = 'poção de vida fraca'
    custo = 15

    def __init__(self):
        super().__init__(30)


class PocaoDeVidaMedia(PocaoDeCura):
    nome = 'poção de vida média'
    custo = 30

    def __init__(self):
        super().__init__(60)


class PocaoDeVidaGrande(PocaoDeCura):
    nome = 'poção de vida grande'
    custo = 45

    def __init__(self):
        super().__init__(90)


class PocaoDeVidaExtraGrande(PocaoDeCura):
    nome = 'poção de vida extra grande'
    custo = 60

    def __init__(self):
        super().__init__(120)


# elixir deve regenerar porcentagem de vida. implementar isso futuramente.
class ElixirDeVidaFraca(PocaoDeCura):
    nome = 'elixir de vida fraca'
    custo = 100

    def __init__(self):
        super().__init__(150)


class ElixirDeVidaMedia(PocaoDeCura):
    nome = 'elixir de vida média'
    custo = 200

    def __init__(self):
        super().__init__(180)


class ElixirDeVidaGrande(PocaoDeCura):
    nome = 'elixir de vida grande'
    custo = 300

    def __init__(self):
        super().__init__(210)


class ElixirDeVidaExtraGrande(PocaoDeCura):
    nome = 'elixir de vida extra grande'
    custo = 400

    def __init__(self):
        super().__init__(240)


curas = [
    PocaoDeVidaFraca, PocaoDeVidaMedia, PocaoDeVidaGrande,
    PocaoDeVidaExtraGrande, ElixirDeVidaFraca, ElixirDeVidaMedia,
    ElixirDeVidaGrande, ElixirDeVidaExtraGrande
]
