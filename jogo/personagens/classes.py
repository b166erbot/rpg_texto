from asyncio import sleep
from collections import Counter
from copy import copy
from functools import reduce
from itertools import chain, combinations, groupby
from random import randint
from time import sleep as sleep2

from jogo.itens.itens import CalcularBonus, SemItemEquipado
from jogo.itens.moedas import Draconica, Glifos, Pratas
from jogo.itens.pocoes import curas
from jogo.itens.quest import ItemQuest
from jogo.pets import SemPet
from jogo.tela.imprimir import Imprimir, formatar_status
from jogo.utils import Acumulador, Contador, arrumar_porcentagem, chunk, regra_3

tela = Imprimir()


class Humano:
    """
    Classe geral para cada classe de personagem no jogo.

    o que os atributos aumentão?
    vitalidade - vida
    fortividade - dano físico
    resistência - resistência a magia[
        fogo, gelo, raio, veneno, magia do submundo
    ]
    inteligência - dano mágico
    crítico - dano crítico
    destreza - velocidade ataque, habilidade com armas
    movimentação - velocidade movimentação
    """

    def __init__(
        self,
        nome,
        jogador=False,
        level=1,
        status={},
        experiencia=0,
        moedas={},
        peitoral=SemItemEquipado("Peitoral", "Peitoral", "Peitoral"),
        elmo=SemItemEquipado("Elmo", "Elmo", "Elmo"),
        calca=SemItemEquipado("Calça", "Calça", "Calça"),
        botas=SemItemEquipado("Botas", "Botas", "Botas"),
        luvas=SemItemEquipado("Luvas", "Luvas", "Luvas"),
        arma=SemItemEquipado("Arma", "Arma", "Arma"),
        anel=SemItemEquipado("Anel", "Anel", "Anel"),
        amuleto=SemItemEquipado("Amuleto", "Amuleto", "Amuleto"),
        item_secundario=SemItemEquipado(
            "Item secundário", "Item secundário", "Item secundário"
        ),
        adorno_de_arma=SemItemEquipado(
            "Adorno de arma", "Adorno de arma", "Adorno de arma"
        ),
    ):
        self.nome = nome.split()[0][:20]
        self.nome_completo = nome
        self.level = level
        leveis = [4999, 9999, 14999, 19999, 24999, 29999, 34999, 39999]
        self.experiencia = Acumulador(experiencia, leveis, level)
        self.status = Counter(
            status
            or {
                "vida": 100,
                "dano": 5,
                "resistencia": 0,
                "velo-ataque": 1,
                "criti": 0,
                "armadura": 0,
                "magia": 100,
                "stamina": 100,
                "velo-movi": 1,
            }
        )
        self._status = copy(self.status)
        self.habilidades = {}
        self.inventario = []
        self.moedas = moedas or {"Pratas": 1500, "Draconica": 0, "Glifos": 0}
        self.moedas["Pratas"] = Pratas(self.moedas["Pratas"])
        self.moedas["Draconica"] = Draconica(self.moedas["Draconica"])
        self.moedas["Glifos"] = Glifos(self.moedas["Glifos"])
        self.jogador = jogador
        self.equipamentos = {
            "Peitoral": peitoral,
            "Elmo": elmo,
            "Calça": calca,
            "Botas": botas,
            "Luvas": luvas,
            "Arma": arma,
            "Anel": anel,
            "Amuleto": amuleto,
            "Item secundário": item_secundario,
            "Adorno de arma": adorno_de_arma,
        }
        self.quests = []
        porcentagem = enumerate([42, 84, 126, 168, 210, 252, 294, 336], 1)
        self._porcentagem_total = dict(porcentagem)
        self.porcentagem_armadura = 0
        self.porcentagem_resistencia = 0
        self.porcentagem_critico = 0
        self.aumento_dano_critico = 2.0
        self.valor_de_bloqueio = 0
        self._calcular_bonus = CalcularBonus(self)
        self._contador = Contador(4)
        self.pet_equipado = SemPet()
        self.atualizar_status()

    @property
    def vida_maxima(self):
        """Método que retorna a vida máxima."""
        equipamentos = filter(lambda x: x, self.equipamentos.values())
        equipamentos = filter(
            lambda x: x.tipo
            in [
                "Elmo",
                "Peitoral",
                "Calça",
                "Luvas",
                "Botas",
                "Anel",
                "Amuleto",
                "Escudo",
            ],
            equipamentos,
        )
        vida = map(lambda x: x.vida, equipamentos)
        vida = self._status["vida"] + (15 * (self.level - 1)) + sum(vida)
        return vida

    def atacar(self, other):
        """Método que escolhe se ataca como bot ou não."""
        if self.jogador:
            return self._atacar_como_jogador(other)
        return self._atacar_como_bot(other)

    async def _atacar_como_bot(self, other):
        """Método que ataca como bot."""
        while all([other.status["vida"] > 0, self.status["vida"] > 0]):
            self.consumir_pocoes()
            if randint(0, 2) == 2:
                habilidade = self.habilidades[randint(1, 2)]
                if self.consumir_magia_stamina():
                    habilidade(other)
                    self._contador.resetar()
            else:
                self._dar_dano_padrao(other)
                other.arrumar_vida()
                self._contador.acrescentar()
            if self._contador.usar:
                self._recuperar_magia_stamina()
            tela.imprimir_combate(formatar_status(self), self)
            await sleep(0.2)
        tela.imprimir_combate(formatar_status(self), self)
        await sleep(1)

    async def _atacar_como_jogador(self, other):
        """Método que ataca como jogador."""
        while all([other.status["vida"] > 0, self.status["vida"] > 0]):
            self.consumir_pocoes()
            caracter = tela.obter_caracter()
            if caracter != -1:
                caracter = chr(caracter)
                if caracter in ["1", "2"] and self.consumir_magia_stamina():
                    habilidade = self.habilidades[caracter]
                    habilidade(other)
                    self._contador.resetar()
                else:
                    self._dar_dano_padrao(other)
                    self._contador.acrescentar()
            else:
                self._dar_dano_padrao(other)
                self._contador.acrescentar()
            if self._contador.usar:
                self._recuperar_magia_stamina()
            other.arrumar_vida()
            tela.imprimir_combate(formatar_status(self), 1)
            await sleep(0.5)
        tela.imprimir_combate(formatar_status(self), 1)
        await sleep(0.5)

    def _dar_dano_padrao(self, other):
        """Método que dá o dano padrão."""
        dano = self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def arrumar_vida(self):
        """Método que arruma a vida para não sair do limite permitido."""
        if self.status["vida"] < 0:
            self.status["vida"] = 0
        if self.status["vida"] > self.vida_maxima:
            self.status["vida"] = self.vida_maxima

    def ressucitar(self):
        """Método que ressucita o personagem."""
        self.status["vida"] = self.vida_maxima

    def consumir_pocoes(self):
        """Método que consome a poção caso você tenha."""
        porcentagem = (self.status["vida"] * 100) // self.vida_maxima
        if porcentagem <= 30:
            pocao = self._dropar_pocoes()
            if bool(pocao):
                self.status["vida"] += pocao.consumir(self.vida_maxima)
                self.arrumar_vida()

    def _dropar_pocoes(self) -> list:
        """Método que retorna uma poção caso você tenha."""
        pilhas_de_pocoes = list(
            filter(lambda x: x.tipo == "Pilha de Poções", self.inventario)
        )
        pocao = False
        while bool(pilhas_de_pocoes):
            pilha = pilhas_de_pocoes[0]
            pocao = pilha.retornar_pocao()
            if not bool(pocao):
                index = self.inventario.index(pilha)
                self.inventario.pop(index)
            else:
                break
            pilhas_de_pocoes = list(
                filter(lambda x: x.tipo == "Pilha de Poções", self.inventario)
            )
        if bool(pilhas_de_pocoes):
            if len(pilha) == 0:
                index = self.inventario.index(pilha)
                self.inventario.pop(index)
        return pocao

    def juntar_pocoes(self):
        pocoes = [
            pilha
            for pilha in self.inventario
            if pilha.tipo == "Pilha de Poções"
        ]
        grupos = groupby(pocoes, key=lambda x: x.nome)
        for key, grupo in grupos:
            grupo = list(grupo)
            tamanho = len(grupo)
            while bool(grupo):
                # aqui o combinations verifica qual combinação dá uma soma igual a 10
                lista = [
                    combinations(grupo, numero)
                    for numero in range(2, len(grupo) + 1)
                ]
                lista = chain(*lista)
                for itens in lista:
                    itens = list(itens)
                    if sum([len(item) for item in itens]) == 10:
                        grupo2 = reduce(lambda x, y: x.juntar_pilha(y), itens)
                        for item in itens:
                            index = grupo.index(item)
                            grupo.pop(index)
                            index = self.inventario.index(item)
                            self.inventario.pop(index)
                        self.inventario.append(grupo2)
                grupo_de_10 = list(filter(lambda x: len(x) == 10, grupo))
                for pilha in grupo_de_10:
                    index = grupo.index(pilha)
                    grupo.pop(index)
                    index = self.inventario.index(pilha)
                    self.inventario.pop(index)
                    self.inventario.append(pilha)
                if len(grupo) == tamanho:
                    grupo2 = reduce(lambda x, y: x.juntar_pilha(y), grupo)
                    for item in grupo:
                        index = self.inventario.index(item)
                        self.inventario.pop(index)
                    self.inventario.append(grupo2)
                    break
                else:
                    tamanho = len(grupo)

    def recuperar_magia_stamina_cem_porcento(self):
        """Método que recupera a magia e stamina para máximo."""
        self.status["magia"] = 100
        self.status["stamina"] = 100

    def desequipar(self, equipamento):
        """Método que desequipa um item no inventário."""
        equipamento2 = self.equipamentos.get(equipamento.tipo_equipar)
        if equipamento2 and equipamento2 is equipamento:
            if self.e_possivel_guardar(equipamento):
                self.guardar_item(equipamento)
                self.equipamentos[equipamento.tipo_equipar] = SemItemEquipado(
                    equipamento.nome,
                    equipamento.tipo,
                    equipamento.tipo_equipar,
                )
                self.atualizar_status()
            else:
                tela.imprimir(
                    "não foi possível adicionar item ao inventario, "
                    "inventario cheio.\n"
                )
                sleep2(3)

    def equipar(self, equipamento):
        raise NotImplementedError("Método não implementado.")

    def atualizar_status(self):
        """Método que atualiza o status."""
        self.level = self.experiencia.level
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        # nos equipamentos tipo "Arma" já pega o item secundário.
        equipamentos_dano = filter(
            lambda x: x.tipo in ["Anel", "Arma", "Amuleto"], equipamentos
        )
        dano = map(lambda x: x.dano, equipamentos_dano)
        dano = self._status["dano"] + sum(dano)
        vida = self.vida_maxima
        self.status["vida"] = vida
        self.status["resistencia"] = self._resistencia
        self.status["armadura"] = self._armadura
        self.status["dano"] = dano
        self.status["critico"] = self._critico
        self.aumento_dano_critico = self._aumento_critico
        self.valor_de_bloqueio = self._bloqueio
        self.pet_equipado.calcular_bonus(self)
        self._calcular_bonus.calcular(self.equipamentos.values())
        self.atualizar_porcentagem()

    def atualizar_porcentagem(self):
        """Método que atualiza as porcentagens."""
        self.porcentagem_armadura = arrumar_porcentagem(
            regra_3(self._porcentagem_total[self.level], 100, self._armadura)
        )
        self.porcentagem_resistencia = arrumar_porcentagem(
            regra_3(
                self._porcentagem_total[self.level],
                100,
                self._resistencia,
            )
        )
        self.porcentagem_critico = arrumar_porcentagem(
            regra_3(
                self._porcentagem_total[self.level],
                100,
                self._critico,
            )
        )

    def e_possivel_guardar(self, item):
        """Método que retorna se é possível guardar item."""
        itens = list(
            filter(lambda x: not isinstance(x, ItemQuest), self.inventario)
        )
        if isinstance(item, ItemQuest):
            return True
        elif len(itens) < 30:
            return True
        else:
            return False

    def guardar_item(self, item):
        """Método que guarda um item no inventario se possível."""
        self.inventario.append(item)

    @property
    def _armadura(self):
        """Método que retorna a armadura dos equipamentos."""
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        tipos = [
            "Elmo",
            "Peitoral",
            "Calça",
            "Luvas",
            "Botas",
            "Anel",
            "Amuleto",
            "Escudo",
        ]
        vestes = filter(lambda x: x.tipo in tipos, equipamentos)
        armadura = self._status["armadura"] + sum(
            map(lambda x: x.armadura, vestes)
        )
        return armadura

    @property
    def _resistencia(self):
        """Método que retorna a resistencia dos equipamentos."""
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        tipos = [
            "Elmo",
            "Peitoral",
            "Calça",
            "Luvas",
            "Botas",
            "Anel",
            "Amuleto",
            "Escudo",
        ]
        vestes = filter(lambda x: x.tipo in tipos, equipamentos)
        resistencia = self._status["resistencia"] + sum(
            map(lambda x: x.resistencia, vestes)
        )
        return resistencia

    @property
    def _critico(self):
        """Método que retorna o valor critico dos equipamentos."""
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        itens_critico = filter(
            lambda x: x.tipo in ["Arma", "Adorno de arma"], equipamentos
        )
        critico = self._status["critico"] + sum(
            map(lambda x: x.critico, itens_critico)
        )
        return critico

    @property
    def _aumento_critico(self):
        """Método que retorna o aumento do dano critico"""
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        itens_aumento_critico = filter(
            lambda x: x.tipo in ["Arma", "Adorno de arma"], equipamentos
        )
        aumento_critico = sum(
            map(lambda x: x.aumento_critico, itens_aumento_critico)
        )
        aumento_critico = aumento_critico / 100 + 2
        return aumento_critico

    @property
    def _bloqueio(self):
        """Método que retorna o valor de bloqueio do personagem"""
        equipamento = self.equipamentos["Item secundário"]
        if equipamento.tipo == "Escudo":
            return equipamento.bloqueio // 100
        else:
            return 0

    def _recuperar_magia_stamina(self):
        if self.status["magia"] <= 80:
            self.status["magia"] += 20
        elif self.status["stamina"] <= 80:
            self.status["stamina"] += 20

    def atualizar_porcentagem_por_level(self, level):
        """Método que atualiza a porcentagem dependendo do level do inimigo."""
        self.porcentagem_armadura -= 8 * level
        self.porcentagem_resistencia -= 8 * level
        if self.porcentagem_armadura < 0:
            self.porcentagem_armadura = 0
        if self.porcentagem_resistencia < 0:
            self.porcentagem_resistencia = 0


class Arqueiro(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.tres_flechas, self.flecha_de_fogo]
        self.habilidades_nomes = ["três flexas", "flecha de fogo"]
        self.habilidades = {str(x): y for x, y in enumerate(habilidades, 1)}
        self.classe = "Arqueiro"

    def tres_flechas(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (5 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 5 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def flecha_de_fogo(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (10 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 10 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        if equipamento.classe in ["Todos", "Arqueiro"]:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo_equipar]):
                self.inventario.append(
                    self.equipamentos[equipamento.tipo_equipar]
                )
            self.equipamentos[equipamento.tipo_equipar] = equipamento
            self.atualizar_status()


class Guerreiro(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.investida, self.esmagar]
        self.habilidades_nomes = ["investida", "esmagar"]
        self.habilidades = {str(x): y for x, y in enumerate(habilidades, 1)}
        self.classe = "Guerreiro"

    def investida(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (5 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 5 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def esmagar(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (10 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 10 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        if equipamento.classe in ["Todos", "Guerreiro"]:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo_equipar]):
                self.inventario.append(
                    self.equipamentos[equipamento.tipo_equipar]
                )
            self.equipamentos[equipamento.tipo_equipar] = equipamento
            self.atualizar_status()


class Mago(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.lanca_de_gelo, self.bola_de_fogo]
        self.habilidades_nomes = ["lanca de gelo", "bola de fogo"]
        self.habilidades = {str(x): y for x, y in enumerate(habilidades, 1)}
        self.classe = "Mago"

    def lanca_de_gelo(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (5 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 5 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano

    def bola_de_fogo(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (10 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 10 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["magia"] >= 20:
            self.status["magia"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        if equipamento.classe in ["Todos", "Mago"]:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo_equipar]):
                self.inventario.append(
                    self.equipamentos[equipamento.tipo_equipar]
                )
            self.equipamentos[equipamento.tipo_equipar] = equipamento
            self.atualizar_status()


class Assassino(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.lancar_faca, self.ataque_furtivo]
        self.habilidades_nomes = ["lancar faca", "ataque furtivo"]
        self.habilidades = {str(x): y for x, y in enumerate(habilidades, 1)}
        self.classe = "Assassino"

    def lancar_faca(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (5 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 5 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def ataque_furtivo(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (10 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 10 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        if equipamento.classe in ["Todos", "Assassino"]:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo_equipar]):
                self.inventario.append(
                    self.equipamentos[equipamento.tipo_equipar]
                )
            self.equipamentos[equipamento.tipo_equipar] = equipamento
            self.atualizar_status()


class Clerigo(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.curar, self.luz]
        self.habilidades_nomes = ["curar", "luz"]
        self.habilidades = {str(x): y for x, y in enumerate(habilidades, 1)}
        self.classe = "Clerigo"

    def curar(self, other):
        """Método que cura o personagem."""
        if randint(1, 100) <= self.porcentagem_critico:
            vida = (10 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            vida = 10 * self.level + self.status["dano"]
        self.status["vida"] += vida
        self.arrumar_vida()

    def luz(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (5 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 5 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["magia"] >= 20:
            self.status["magia"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        if equipamento.classe in ["Todos", "Mago"]:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo_equipar]):
                self.inventario.append(
                    self.equipamentos[equipamento.tipo_equipar]
                )
            self.equipamentos[equipamento.tipo_equipar] = equipamento
            self.atualizar_status()


class Monge(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.multiplos_socos, self.combo_de_chutes]
        self.habilidades_nomes = ["multiplos_socos", "combo_de_chutes"]
        self.habilidades = {str(x): y for x, y in enumerate(habilidades, 1)}
        self.classe = "Monge"

    def multiplos_socos(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (5 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 5 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def combo_de_chutes(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (10 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 10 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        if equipamento.classe in ["Todos", "Monge"]:
            # tira o equipamento do inventario
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            # se tiver equipamento equipado, mova-o para o inventario
            if bool(self.equipamentos[equipamento.tipo_equipar]):
                self.inventario.append(
                    self.equipamentos[equipamento.tipo_equipar]
                )
            # equipa o equipamento
            self.equipamentos[equipamento.tipo_equipar] = equipamento
        self.atualizar_status()


class Druida(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.invocando_galhos_do_chao, self.grito_da_floresta]
        self.habilidades_nomes = [
            "invocando_galhos_do_chão",
            "grito_da_floresta",
        ]
        self.habilidades = {str(x): y for x, y in enumerate(habilidades, 1)}
        self.classe = "Druida"

    def invocando_galhos_do_chao(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (5 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 5 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def grito_da_floresta(self, other):
        """Método que ataca o oponente."""
        if randint(1, 100) <= self.porcentagem_critico:
            dano = (10 * self.aumento_dano_critico * self.level) + self.status[
                "dano"
            ]
        else:
            dano = 10 * self.level + self.status["dano"]
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["magia"] >= 20:
            self.status["magia"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        if equipamento.classe in ["Todos", "Druida"]:
            # tira o equipamento do inventario
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            # se tiver equipamento equipado, mova-o para o inventario
            if bool(self.equipamentos[equipamento.tipo_equipar]):
                self.inventario.append(
                    self.equipamentos[equipamento.tipo_equipar]
                )
            # equipa o equipamento
            self.equipamentos[equipamento.tipo_equipar] = equipamento
        self.atualizar_status()


# dual blade?
