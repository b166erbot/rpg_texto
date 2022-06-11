from asyncio import sleep
from collections import Counter
from random import choice, randint

from jogo.itens.armas import Arma
from jogo.itens.armas import tudo as armas
from jogo.itens.vestes import Anel, Roupa
from jogo.itens.vestes import tudo as vestes
from jogo.tela.imprimir import Imprimir, efeito_digitando, formatar_status

tela = Imprimir()


class Monstro:
    def __init__(self, nivel=1, status={}):
        self.experiencia = 500 * nivel
        self.status = Counter(
            status
            or {
                "vida": 100,
                "dano": 3,
                "resis": 5,
                "velo-ataque": 1,
                "critico": 5,
                "armadura": 5,
                "magia": 100,
                "stamina": 100,
                "velo-movi": 1,
            }
        )
        for item in self.status:
            if item in ["magia", "stamina"]:
                continue
            self.status[item] *= nivel
        self.habilidades = []
        self.vida_ = self.status["vida"]
        self.nivel = nivel

    async def atacar(self, other):
        """Método que ataca como bot o personagem."""
        while all([other.status["vida"] > 0, self.status["vida"] > 0]):
            dano = self.status["dano"]
            other.receber_dano(dano, self.tipo_dano)
            if randint(0, 2) == 2:
                habilidade = choice(self.habilidades)
                if self.status["stamina"] >= 20:
                    self.status["stamina"] -= 20
                    habilidade(other)
            other.arrumar_vida()
            tela.imprimir_combate(formatar_status(self), 2)
            await sleep(0.5)
        tela.imprimir_combate(formatar_status(self), 2)
        await sleep(0.5)

    def ressucitar(self):
        """Método que ressucita."""
        self.status["vida"] = self.vida_

    @property
    def vida_maxima(self):
        """Método que retorna a vida máxima."""
        return self.vida_

    def arrumar_vida(self):
        """Método que arruma a vida."""
        if self.status["vida"] < 0:
            self.status["vida"] = 0
        if self.status["vida"] > self.vida_maxima:
            self.status["vida"] = self.vida_maxima

    def sortear_drops(self, personagem):
        """Método que dá item e pratas ao personagem."""
        if randint(0, 2) == 1:
            efeito_digitando("Loot encontrado.")
            Item = choice(vestes + armas)
            if issubclass(Item, Arma):
                status = [randint(1, 5), randint(1, 2), randint(1, 3)]
                status = map(lambda x: x * self.nivel, status)
                status_nomes = ["dano", "velo_ataque", "critico"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            elif issubclass(Item, Roupa):
                status = [
                    randint(1, 3), randint(1, 3), randint(5, 20), randint(1, 3)
                ]
                status = map(lambda x: x * self.nivel, status)
                status_nomes = ["armadura", "velo_movi", "vida", "resistencias"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            elif issubclass(Item, Anel):
                status = [
                    randint(1, 3), randint(5, 20), randint(1, 3), randint(1, 3)
                ]
                status = map(lambda x: x * self.nivel, status)
                status_nomes = ["dano", "vida", "resistencias", "armadura"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(nome="Anel", **status_dict)
            personagem.pratas += randint(30 * self.nivel, 50 * self.nivel)
            personagem.inventario.append(item)


class Boss(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experiencia *= 2

    def dar_loot_boss(self, personagem):
        """Método que dá item e pratas ao personagem."""
        efeito_digitando("Loot encontrado.")
        Item = choice(vestes + armas)
        if issubclass(Item, Arma):
            status = [randint(3, 5), randint(2, 2), randint(2, 3)]
            status = map(lambda x: x * self.nivel, status)
            status_nomes = ["dano", "velo_ataque", "critico"]
            status_dict = dict(zip(status_nomes, status))
            item = Item(**status_dict)
        elif issubclass(Item, Roupa):
            status = [
                randint(2, 3), randint(2, 3), randint(12, 20), randint(2, 3)
            ]
            status = map(lambda x: x * self.nivel, status)
            status_nomes = ["armadura", "velo_movi", "vida", "resistencias"]
            status_dict = dict(zip(status_nomes, status))
            item = Item(**status_dict)
        elif issubclass(Item, Anel):
            status = [
                randint(2, 3), randint(12, 20), randint(2, 3), randint(2, 3)
            ]
            status = map(lambda x: x * self.nivel, status)
            status_nomes = ["dano", "vida", "resistencias", "armadura"]
            status_dict = dict(zip(status_nomes, status))
            item = Item(nome="Anel", **status_dict)
        personagem.pratas += randint(30 * self.nivel, 50 * self.nivel)
        personagem.inventario.append(item)


class Tartaruga(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.investida, self.garras_afiadas]
        self.nome = "Tartaruga"
        self.classe = "Monstro comum"
        self.tipo = "Tatu bola"
        self.tipo_dano = "fisico"

    def investida(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(4 * self.nivel, self.tipo_dano)

    def garras_afiadas(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(6 * self.nivel, self.tipo_dano)


class Camaleao(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.trapasseiro, self.roubo]
        self.nome = "Camaleão"
        self.classe = "Monstro comum"
        self.tipo = "trolador"
        self.tipo_dano = "fisico"

    def trapasseiro(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(4 * self.nivel, self.tipo_dano)

    def roubo(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(5 * self.nivel, self.tipo_dano)


class Tamandua(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.abraco, self.linguada]
        self.nome = "Tamandua"
        self.classe = "Monstro comum"
        self.tipo = "trolador"
        self.tipo_dano = "fisico"

    def abraco(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(5 * self.nivel, self.tipo_dano)

    def linguada(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(3 * self.nivel, self.tipo_dano)


class Sapo(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.salto, self.linguada]
        self.nome = "Sapo"
        self.classe = "Monstro comum"
        self.tipo = "trolador"
        self.tipo_dano = "magico"

    def salto(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(5 * self.nivel, self.tipo_dano)

    def linguada(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(3 * self.nivel, self.tipo_dano)


class Topera(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.pulo_fatal, self.terremoto]
        self.nome = "Topera"
        self.classe = "Monstro chefe"
        self.tipo = "boss"
        self.tipo_dano = "fisico"

    def pulo_fatal(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(7 * self.nivel, self.tipo_dano)

    def terremoto(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(10 * self.nivel, self.tipo_dano)


class Mico(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.tacar_banana, self.esmagar]
        self.nome = "Mico"
        self.classe = "Monstro chefe"
        self.tipo = "boss"
        self.tipo_dano = "magico"

    def tacar_banana(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(10 * self.nivel, self.tipo_dano)

    def esmagar(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(15 * self.nivel, self.tipo_dano)


class Sucuri(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.lancamento_de_calda, self.bote]
        self.nome = "Sucuri"
        self.classe = "Monstro chefe"
        self.tipo = "boss"
        self.tipo_dano = "magico"

    def lancamento_de_calda(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(10 * self.nivel, self.tipo_dano)

    def bote(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(15 * self.nivel, self.tipo_dano)


class ArvoreDeku(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.braçada, self.outono]
        self.nome = "Arvore Deku"
        self.classe = "Monstro chefe"
        self.tipo = "boss"
        self.tipo_dano = "fisico"

    def braçada(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(10 * self.nivel, self.tipo_dano)

    def outono(self, other):
        """Método que ataca o personagem."""
        other.receber_dano(15 * self.nivel, self.tipo_dano)


monstros_comuns = [Tartaruga, Camaleao, Tamandua, Sapo]
bosses = [Topera, Mico, Sucuri, ArvoreDeku]
