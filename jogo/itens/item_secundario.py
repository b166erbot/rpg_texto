from jogo.itens.moedas import Pratas


class ItemDeDefesa:
    # tipo precisa ficar aqui em cima
    tipo = "Escudo"

    def __init__(
        self,
        nome: str,
        vida: int,
        armadura: int,
        resistencia: int,
        bloqueio: int,
        classe: str,
    ):
        self.nome = nome
        self.vida = vida
        self.armadura = armadura
        self.resistencia = resistencia
        self.bloqueio = bloqueio
        self.classe = classe
        self.tipo_equipar = "Item secundário"
        self.bonus = []
        self.preco = Pratas(((vida // 2) + armadura + resistencia) * 8)
        self.conjunto = "item comum"

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura})"
        )
        return retorno


class ItemDeDano:
    # tipo precisa ficar aqui em cima
    tipo = "Arma"

    def __init__(
        self,
        nome: str,
        dano: int,
        critico: int,
        porcentagem_critico: int,
        classe: str,
    ):
        self.nome = nome
        self.dano = dano
        self.critico = critico
        self.porcentagem_critico = porcentagem_critico
        self.classe = classe
        self.tipo_equipar = "Item secundário"
        self.bonus = []
        self.preco = Pratas((dano + critico + (porcentagem_critico // 2)) * 8)
        self.conjunto = "item comum"

    def __repr__(self):
        retorno = (
            f"{self.nome}(dan: {self.dano}, crit: {self.critico}"
            f", crit porc: {self.porcentagem_critico})"
        )
        return retorno


class Escudo(ItemDeDefesa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Escudo", classe="Guerreiro", **kwargs)


class BolaDeCristal(ItemDeDefesa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Bola de cristal", classe="Mago", **kwargs)


class Livro(ItemDeDano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Livro", classe="Mago", **kwargs)


# buckler: um pequeno escudo redondo segurado por uma alça ou usado no antebraço.
class Buckler(ItemDeDefesa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Buckler", classe="Arqueiro", **kwargs)


class Aljava(ItemDeDano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Aljava", classe="Arqueiro", **kwargs)


class Adaga(ItemDeDano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Adaga", classe="Assassino", **kwargs)


tudo = [Escudo, BolaDeCristal, Livro, Buckler, Aljava, Adaga]
