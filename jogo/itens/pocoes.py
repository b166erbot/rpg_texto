from jogo.itens.moedas import Pratas


class PilhaDePocoes:
    def __init__(self, pocoes: list, nome: str):
        self.pocoes = pocoes
        self.nome = nome
        self.tipo = "Pilha de Poções"
        self.classe = "Pilha de Poções"
        self.numero_maximo_pocoes = 10
        if len(pocoes) > 10:
            raise Exception('Excedeu o valor máximo de poções')

    def retornar_pocao(self):
        if len(self.pocoes) >= 0:
            return self.pocoes.pop()
        else:
            return False

    def e_possivel_juntar(self, other):
        condicoes = [
            self.tipo == other.tipo,
            (
                len(self.pocoes)
                + len(other.pocoes)
                <= self.numero_maximo_pocoes
            )
        ]
        if all(condicoes):
            return True
        else:
            return False

    def juntar_pilha(self, other):
        pocoes = self.pocoes + other.pocoes
        return self.__class__(pocoes, self.nome)
    
    def e_possivel_adicionar_pocao(self):
        if len(self.pocoes) < self.numero_maximo_pocoes:
            return True
        else:
            return False
    
    def adicionar_pocao(self, pocao):
        self.pocoes.append(pocao)
    
    def __len__(self):
        return len(self.pocoes)

    def __repr__(self):
        retorno = (
            f"pilha de poções({self.nome}, {len(self)})"
        )
        return retorno


class PocaoDeCura:
    tipo = "Poções"

    def __init__(self, pontos_cura: int):
        self.pontos_cura = pontos_cura
        self.classe = "Poções"
        self.consumida = False

    def __repr__(self):
        retorno = (
            f"{self.nome.capitalize()} - "
            f"Cura: {self.pontos_cura}"
        )
        return retorno

    def consumir(self, vida_maxima):
        """Método que consome a poção."""
        # a variável vida_maxima neste método não tem propósito mas é necessária, favor não remover.
        if self.consumida == False:
            self.consumida = True
            return self.pontos_cura
        return 0


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
        self.consumida = False

    def __repr__(self):
        retorno = (
            f"{self.nome.capitalize()} - "
            f"Cura: {self.porcentagem}%"
        )
        return retorno

    def consumir(self, vida_maxima):
        """Método que consome a poção."""
        if self.consumida == False:
            self.consumida = True
            return (self.porcentagem * vida_maxima) // 100
        return 0


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
