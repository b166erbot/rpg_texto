from jogo.itens.moedas import Pratas


class PocaoDeCura:
    tipo = "Poções"

    def __init__(self, pontos_cura: int):
        self.pontos_cura = pontos_cura
        self.classe = "Poções"
        self.numero_maximo_pocoes = 10
        self.numero_de_pocoes = 1

    def __repr__(self):
        retorno = (
            f"{self.nome.capitalize()} - "
            f"Cura: {self.pontos_cura}, "
            f"unidade: {self.numero_de_pocoes}"
        )
        return retorno

    def consumir(self, vida_maxima):
        """Método que consome a poção."""
        # a variável vida_maxima neste método não tem propósito mas é necessária, favor não remover.
        if self.numero_de_pocoes > 0:
            self.numero_de_pocoes -= 1
            return self.pontos_cura
        return 0

    def juntar(self, personagem, pocao):
        condicoes = [
            isinstance(pocao, self.__class__),
            self.numero_de_pocoes < self.numero_maximo_pocoes,
        ]
        if all(condicoes):
            self.numero_de_pocoes += 1
            index = personagem.inventario.index(pocao)
            personagem.inventario.pop(index)
        return self


class PocaoDeVidaFraca(PocaoDeCura):
    nome = "poção de vida fraca"
    preco = Pratas(15)
    quanto_cura = "30"

    def __init__(self):
        super().__init__(30)


class PocaoDeVidaMedia(PocaoDeCura):
    nome = "poção de vida média"
    preco = Pratas(30)
    quanto_cura = "60"

    def __init__(self):
        super().__init__(60)


class PocaoDeVidaGrande(PocaoDeCura):
    nome = "poção de vida grande"
    preco = Pratas(45)
    quanto_cura = "90"

    def __init__(self):
        super().__init__(90)


class PocaoDeVidaExtraGrande(PocaoDeCura):
    nome = "poção de vida extra grande"
    preco = Pratas(60)
    quanto_cura = "120"

    def __init__(self):
        super().__init__(120)


class Elixir:
    tipo = "Poções"

    def __init__(self, porcentagem: int):
        self.porcentagem = porcentagem
        self.classe = "Poções"
        self.numero_maximo_pocoes = 10
        self.numero_de_pocoes = 1

    def __repr__(self):
        retorno = (
            f"{self.nome.capitalize()} - "
            f"Cura: {self.porcentagem}%, "
            f"unidade: {self.numero_de_pocoes}"
        )
        return retorno

    def consumir(self, vida_maxima):
        """Método que consome a poção."""
        if self.numero_de_pocoes > 0:
            self.numero_de_pocoes -= 1
            return (self.porcentagem * vida_maxima) // 100
        return 0

    def juntar(self, personagem, pocao):
        condicoes = [
            isinstance(pocao, self.__class__),
            self.numero_de_pocoes < self.numero_maximo_pocoes,
        ]
        if all(condicoes):
            self.numero_de_pocoes += 1
            index = personagem.inventario.index(pocao)
            personagem.inventario.pop(index)
        return self


class ElixirDeVidaFraca(Elixir):
    nome = "elixir de vida fraca"
    preco = Pratas(100)
    quanto_cura = "20%"

    def __init__(self):
        super().__init__(20)


class ElixirDeVidaMedia(Elixir):
    nome = "elixir de vida média"
    preco = Pratas(200)
    quanto_cura = "40%"

    def __init__(self):
        super().__init__(40)


class ElixirDeVidaGrande(Elixir):
    nome = "elixir de vida grande"
    preco = Pratas(300)
    quanto_cura = "60%"

    def __init__(self):
        super().__init__(60)


class ElixirDeVidaExtraGrande(Elixir):
    nome = "elixir de vida extra grande"
    preco = Pratas(400)
    quanto_cura = "80%"

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
