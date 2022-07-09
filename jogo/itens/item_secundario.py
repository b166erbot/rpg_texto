from jogo.itens.moedas import Glifos, Pratas
from jogo.utils import Acumulador


# a classe precisa ficar em cima pois na hora de dropar o item do monstro ele faz a verificação.
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
        level: int = 1,
    ):
        self.nome = nome
        self.vida = vida * level
        self.armadura = armadura * level
        self.resistencia = resistencia * level
        self.bloqueio = bloqueio
        self._valores_base = {
            "vida": vida,
            "armadura": armadura,
            "resistencia": resistencia,
            "level": level,
        }
        self.tipo_equipar = "Item secundário"
        self.bonus = []
        self.preco = Pratas(((vida // 2) + armadura + resistencia) * 8)
        self.conjunto = "item comum"
        self.glifos = Glifos(12 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura}, lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        return glifos


class ItemDeDano:
    # tipo precisa ficar aqui em cima
    tipo = "Arma"

    def __init__(
        self,
        nome: str,
        dano: int,
        critico: int,
        aumento_critico: int,
        level: int = 1,
    ):
        self.nome = nome
        self.dano = dano * level
        self.critico = critico * level
        self.aumento_critico = aumento_critico * level
        self._valores_base = {
            "dano": dano,
            "critico": critico,
            "aumento_critico": aumento_critico,
            "level": level,
        }
        self.tipo_equipar = "Item secundário"
        self.bonus = []
        self.preco = Pratas((dano + critico + (aumento_critico // 2)) * 8)
        self.conjunto = "item comum"
        self.level = level
        self.glifos = Glifos(12 * level)
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(dan: {self.dano}, crit: {self.critico}"
            f", crit porc: {self.aumento_critico}, lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        return glifos


class Escudo(ItemDeDefesa):
    classe = "Guerreiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Escudo", **kwargs)


class BolaDeCristal(ItemDeDefesa):
    classe = "Mago"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Bola de cristal", **kwargs)


class Livro(ItemDeDano):
    classe = "Mago"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Livro", **kwargs)


# buckler: um pequeno escudo redondo segurado por uma alça ou usado no antebraço.
class Buckler(ItemDeDefesa):
    classe = "Arqueiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Buckler", **kwargs)


class Aljava(ItemDeDano):
    classe = "Arqueiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Aljava", **kwargs)


class Adaga(ItemDeDano):
    classe = "Assassino"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Adaga sec.", **kwargs)


tudo = [Escudo, BolaDeCristal, Livro, Buckler, Aljava, Adaga]
