class PocaoDeCura:
    def __init__(self, pontos_cura: int):
        self.pontos_cura = pontos_cura
        self.consumida = False
        self.tipo = "Poções"

    def __repr__(self):
        return f"{self.nome.capitalize()} - " f"Cura: {self.pontos_cura}"

    def consumir(self, vida_maxima):
        """Método que consome a poção."""
        # a variável vida_maxima neste método não tem função, favor manter.
        if not self.consumida:
            self.consumida = True
            return self.pontos_cura
        return 0


class PocaoDeVidaFraca(PocaoDeCura):
    nome = "poção de vida fraca"
    preco = 15

    def __init__(self):
        super().__init__(30)


class PocaoDeVidaMedia(PocaoDeCura):
    nome = "poção de vida média"
    preco = 30

    def __init__(self):
        super().__init__(60)


class PocaoDeVidaGrande(PocaoDeCura):
    nome = "poção de vida grande"
    preco = 45

    def __init__(self):
        super().__init__(90)


class PocaoDeVidaExtraGrande(PocaoDeCura):
    nome = "poção de vida extra grande"
    preco = 60

    def __init__(self):
        super().__init__(120)


class Elixir:
    def __init__(self, porcentagem: int):
        self.porcentagem = porcentagem
        self.consumida = False
        self.tipo = "Poções"

    def __repr__(self):
        return f"{self.nome.capitalize()} - " f"Cura: {self.porcentagem}%"

    def consumir(self, vida_maxima):
        """Método que consome a poção."""
        if not self.consumida:
            self.consumida = True
            return (self.porcentagem * vida_maxima) // 100
        return 0


class ElixirDeVidaFraca(Elixir):
    nome = "elixir de vida fraca"
    preco = 100

    def __init__(self):
        super().__init__(20)


class ElixirDeVidaMedia(Elixir):
    nome = "elixir de vida média"
    preco = 200

    def __init__(self):
        super().__init__(40)


class ElixirDeVidaGrande(Elixir):
    nome = "elixir de vida grande"
    preco = 300

    def __init__(self):
        super().__init__(60)


class ElixirDeVidaExtraGrande(Elixir):
    nome = "elixir de vida extra grande"
    preco = 400

    def __init__(self):
        super().__init__(80)


curas = [
    PocaoDeVidaFraca,
    PocaoDeVidaMedia,
    PocaoDeVidaGrande,
    PocaoDeVidaExtraGrande,
    ElixirDeVidaFraca,
    ElixirDeVidaMedia,
    ElixirDeVidaGrande,
    ElixirDeVidaExtraGrande,
]
