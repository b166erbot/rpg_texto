from collections import Counter
from asyncio import sleep
from random import randint, choice
from jogo.tela.imprimir import formatar_status, Imprimir
from jogo.itens.moedas import Pratas
from jogo.itens.pocoes import curas
from jogo.itens.vestes import tudo as roupas
from jogo.itens.armas import (
    Espada_longa, Machado, Espada_curta, Cajado, Cajado_negro, Arco_longo,
    Arco_curto, Adaga, Luvas_de_ferro
)

nome_pocoes = list(map(lambda x: x.nome, curas))


tela = Imprimir()


class Humano:
    """
    Classe geral para cada classe no jogo.

    o que os atributos aumentão?
    vitalidade - vida
    fortividade - dano físico
    resistência - resistência a magia[fogo, gelo, raio, veneno, magia do submundo]
    inteligência - dano mágico
    crítico - dano crítico
    destreza - velocidade ataque, habilidade com armas
    movimentação - velocidade movimentação
    """

    def __init__(
        self, nome, jogador=False, level=1, status={}, atributos={},
        experiencia=0, pratas = 0, peitoral = False, elmo = False,
        calca = False, botas = False, luvas = False, arma = False,
        Anel = False
    ):
        self.nome = nome
        self.level = level
        self.experiencia = experiencia
        self.status = Counter(
            status or {
                'vida': 100, 'dano': 5, 'resis': 0, 'velo-ataque': 1,
                'criti': 0, 'armadura': 0, 'magia': 100, 'stamina': 100,
                'velo-movi': 1
            }
        )
        self.atributos = Counter(
            atributos or {
                'vitalidade': 0, 'fortividade': 0, 'inteligência': 0,
                'crítico': 0, 'destreza': 0, 'resistência': 0, 'movimentação': 0
            }
        )
        self.habilidades = {}
        self.inventario = []
        self.pratas = Pratas(pratas or 1500)
        self.jogador = jogador
        self.equipamentos = {
            'Peitoral': peitoral, 'Elmo': elmo, 'Calca': calca, 'Botas': botas,
            'Luvas': luvas, 'Arma': arma, "Anel": Anel
        }
        self.quests = []

    @property
    def vida_maxima(self):
        equipamentos = filter(lambda x: x, self.equipamentos.values())
        equipamentos = filter(
            lambda x: x.tipo in ['Elmo', 'Peitoral', 'Calca', 'Botas', 'Anel'],
            equipamentos
        )
        vida = map(lambda x: x.vida, equipamentos)
        vida = 100 + sum(vida)
        return vida

    def atacar(self, other):
        if self.jogador:
            return self._atacar_como_jogador(other)
        return self._atacar_como_bot(other)

    async def _atacar_como_bot(self, other):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            self._consumir_pocoes_bot()
            dano = self.status['dano']
            other.status['vida'] -= dano
            other.arrumar_vida()
            tela.imprimir_combate(formatar_status(self), self)
            await sleep(0.2)
        tela.imprimir_combate(formatar_status(self), self)
        await sleep(1)

    async def _atacar_como_jogador(self, other):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            self._consumir_pocoes_bot()
            dano = self.status['dano']
            other.status['vida'] -= dano
            caracter = tela.obter_caracter()
            if caracter != -1:
                caracter = int(chr(caracter))
                if caracter in [1, 2]:
                    habilidade = self.habilidades[caracter]
                    if self.consumir_magia_stamina():
                        habilidade(other)
            other.arrumar_vida()
            tela.imprimir_combate(formatar_status(self), 1)
            await sleep(0.5)
        tela.imprimir_combate(formatar_status(self), 1)
        await sleep(0.5)

    def arrumar_vida(self):
        if self.status['vida'] < 0:
            self.status['vida'] = 0
        if self.status['vida'] > self.vida_maxima:
            self.status['vida'] = self.vida_maxima

    def ressucitar(self):
        self.status['vida'] = self.vida_maxima

    def _consumir_pocoes_bot(self):
        if self.status['vida'] <= 30:
            pocao = self._dropar_pocoes()
            if pocao:
                self.status['vida'] += pocao.consumir()
                if self.status['vida'] > self.vida_maxima:
                    self.status['vida'] = self.vida_maxima

    def _dropar_pocoes(self) -> list:
        poções = [x for x in self.inventario if x.nome in nome_pocoes]
        if poções:
            index = self.inventario.index(poções[0])
            poção = self.inventario.pop(index)
            return poção
        return False

    def recuperar_magia_stamina(self):
        self.status['magia'] = 100
        self.status['stamina'] = 100

    def vender(self, equipamento):
        index = self.inventario.index(equipamento)
        if self.equipamentos[equipamento.tipo] is equipamento:
            self.equipamentos[equipamento.tipo] = False
            self.atualizar_status()
        self.pratas += equipamento.preco
        self.inventario.pop(index)

    def desequipar(self, equipamento):
        equipamento2 = self.equipamentos.get(equipamento.tipo)
        if equipamento2 and equipamento2 is equipamento:
            self.equipamentos[equipamento.tipo] = False
            self.atualizar_status()

    def receber_dano(self, dano, tipo):
        if tipo == 'fisico':
            dano_ = dano - self.status['armadura']
        elif tipo == 'magico':
            dano_ = dano - self.status['resis']
        if dano_ < 0:
            dano_ = 0
        self.status['vida'] -= dano_

    def atualizar_status(self):
        equipamentos = list(filter(lambda x: x, self.equipamentos.values()))
        vestes = list(filter(
            lambda x: x.tipo in ['Elmo', 'Peitoral', 'Calca', 'Botas', 'Anel'],
            equipamentos
        ))
        equipamentos_dano = filter(
            lambda x: x.tipo in ['Anel', 'Arma'], equipamentos
        )
        dano = map(lambda x: x.dano, equipamentos_dano)
        dano = 5 + sum(dano)
        vida = map(lambda x: x.vida, vestes)
        vida = 100 + sum(vida)
        resistencia = sum(map(lambda x: x.resistencias, vestes))
        armadura = sum(map(lambda x: x.armadura, vestes))
        self.status['vida'] = vida
        self.status['resis'] = resistencia
        self.status['armadura'] = armadura
        self.status['dano'] = dano


class Arqueiro(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.flecha, self.tres_flechas]
        self.habilidades_nomes = ['flecha', 'três flexas']
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = 'Arqueiro'

    def flecha(self, other):
        other.status['vida'] -= 10 + self.status['dano']

    def tres_flechas(self, other):
        other.status['vida'] -= 15 + self.status['dano']

    def consumir_magia_stamina(self):
        if self.status['stamina'] >= 20:
            self.status['stamina'] -= 20
            return True
        return False

    def repr(self):
        return self.classe

    def equipar(self, equipamento):
        for classe in roupas + [Arco_longo, Arco_curto]:
            if isinstance(equipamento, classe):
                self.equipamentos[equipamento.tipo] = equipamento
                self.atualizar_status()


class Guerreiro(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.investida, self.esmagar]
        self.habilidades_nomes = ['investida', 'esmagar']
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = 'Guerreiro'

    def investida(self, other):
        other.status['vida'] -= 10 + self.status['dano']

    def esmagar(self, other):
        other.status['vida'] -= 15 + self.status['dano']

    def consumir_magia_stamina(self):
        if self.status['stamina'] >= 20:
            self.status['stamina'] -= 20
            return True
        return False

    def equipar(self, equipamento):
        for classe in roupas + [Espada_longa, Espada_curta, Machado]:
            if isinstance(equipamento, classe):
                self.equipamentos[equipamento.tipo] = equipamento
                self.atualizar_status()


class Mago(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.bola_de_fogo, self.lanca_de_gelo]
        self.habilidades_nomes = ['bola de fogo', 'lanca de gelo']
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = 'Mago'

    def bola_de_fogo(self, other):
        other.status['vida'] -= 15 + self.status['dano']

    def lanca_de_gelo(self, other):
        other.status['vida'] -= 10 + self.status['dano']

    def consumir_magia_stamina(self):
        if self.status['magia'] >= 20:
            self.status['magia'] -= 20
            return True
        return False

    def equipar(self, equipamento):
        for classe in roupas + [Cajado, Cajado_negro]:
            if isinstance(equipamento, classe):
                self.equipamentos[equipamento.tipo] = equipamento
                self.atualizar_status()


class Assassino(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.lancar_faca, self.ataque_furtivo]
        self.habilidades_nomes = ['lancar faca', 'ataque furtivo']
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = 'Assassino'

    def lancar_faca(self, other):
        other.status['vida'] -= 10 + self.status['dano']

    def ataque_furtivo(self, other):
        other.status['vida'] -= 15 + self.status['dano']

    def consumir_magia_stamina(self):
        if self.status['stamina'] >= 20:
            self.status['stamina'] -= 20
            return True
        return False

    def equipar(self, equipamento):
        for classe in roupas + [Adaga]:
            if isinstance(equipamento, classe):
                self.equipamentos[equipamento.tipo] = equipamento
                self.atualizar_status()


class Clerigo(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.curar, self.luz]
        self.habilidades_nomes = ['curar', 'luz']
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = 'Clerigo'

    def curar(self, other):
        self.status['vida'] += 25 + self.status['dano']
        if self.status['vida'] >= self.vida_maxima:
            self.status['vida'] = self.vida_maxima

    def luz(self, other):
        other.status['vida'] -= 10 + self.status['dano']

    def consumir_magia_stamina(self):
        if self.status['magia'] >= 20:
            self.status['magia'] -= 20
            return True
        return False

    def equipar(self, equipamento):
        for classe in roupas + [Cajado]:
            if isinstance(equipamento, classe):
                self.equipamentos[equipamento.tipo] = equipamento
                self.atualizar_status()

class Monge(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.combo_de_chutes, self.multiplos_socos]
        self.habilidades_nomes = ['combo_de_chutes', 'multiplos_socos']
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = 'Monge'

    def combo_de_chutes(self, other):
        other.status['vida'] -= 15 + self.status['dano']

    def multiplos_socos(self, other):
        other.status['vida'] -= 10 + self.status['dano']

    def consumir_magia_stamina(self):
        if self.status['stamina'] >= 20:
            self.status['stamina'] -= 20
            return True
        return False

    def equipar(self, equipamento):
        for classe in roupas + [Luvas_de_ferro]:
            if isinstance(equipamento, classe):
                self.equipamentos[equipamento.tipo] = equipamento
                self.atualizar_status()


# druida?
# dual blade?
# lutador? monge?
