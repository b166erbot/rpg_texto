from random import choice, randint
from time import sleep
from typing import Union

from jogo.assincrono.combate import combate
from jogo.personagens.monstros import (
    Dragao,
    bosses_da_floresta,
    monstros_da_floresta,
)
from jogo.tela.imprimir import Imprimir, efeito_digitando

from .areas_fechadas import Caverna, Local

local_str = Union[Local, str]

tela = Imprimir()


def local_linear(passagens: list[str]) -> list[Local]:
    """Função que retorna uma lista com passagens."""
    passagens = list(map(Local, passagens))
    fluxo = [choice(passagens) for _ in range(randint(3, 5))]
    return fluxo


def gerar_fluxo() -> list[local_str]:
    """Função que retorna uma lista com fluxos."""
    passagens = [
        "matagal",
        "area florestada",
        "rio",
        "trilha",
        "gruta",
        "corrego",
    ]
    fluxo = (
        local_linear(passagens)
        + local_linear(passagens)
        + ["caverna"]
        + local_linear(passagens)
        + ["caverna", "boss"]
    )
    return fluxo


class Floresta:
    def __init__(self, nome: str, personagem, level: int):
        self.nome = nome
        self.personagem = personagem
        self._caminhos = gerar_fluxo()
        self.level = level

    def explorar(self):
        """Método que explora uma floresta com o personagem."""
        tela.limpar_tela()
        tela.imprimir(self.nome + "\n")
        for caminho in self._caminhos:
            morto = self.disernir_caminho(caminho)
            if morto == "morto":
                return
        tela.imprimir("voltando para o início da floresta\n")
        for caminho in self._caminhos[-2::-1]:
            morto = self.disernir_caminho(caminho)
            if morto == "morto":
                return
        sleep(1)

    def disernir_caminho(self, caminho: Local):
        """Método que diserne o que tem que ser feito dependendo do caminho."""
        efeito_digitando(str(caminho))
        if str(caminho) == "caverna":
            tela.imprimir("deseja entrar na caverna? s/n\n")
            if tela.obter_string().lower() in ["s", "sim"]:
                caverna = Caverna("poço azul", self.personagem, self.level)
                caverna.explorar()
                self.personagem.recuperar_magia_stamina_cem_porcento()
                self.personagem.ressucitar()
                tela.imprimir("saindo da caverna\n")
                sleep(2)
            tela.limpar_tela()
        elif str(caminho) == "boss":
            tela.limpar_tela()
            status = {
                "vida": 300,
                "dano": 5,
                "resistencia": 15,
                "velo-ataque": 1,
                "critico": 15,
                "armadura": 15,
                "magia": 100,
                "stamina": 100,
                "velo-movi": 1,
            }
            Boss = choice(bosses_da_floresta)
            boss = Boss(self.level, status)
            tela.imprimir("Boss encontrado.\n")
            tela.imprimir(str(boss) + "\n")
            lutar = self._lutar_ou_fugir()
            if lutar:
                combate(self.personagem, boss)
                if self.personagem.morto():
                    self.morto()
                    return "morto"
                else:
                    boss.dar_experiencia(self.personagem)
                    boss.sortear_drops(self.personagem)
                    boss.sortear_drops_quest(self.personagem)
                self.personagem.recuperar_magia_stamina_cem_porcento()
        morte = self.sortear_inimigos()
        if morte:
            self.morto()
            return "morto"
        self.sortear_drop_quest_mapa()
        morte = self._sortear_boss_dragao()
        if morte:
            self.morto()
            return "morto"

    def sortear_inimigos(self):
        """Método que sorteia os inimigos para o personagem."""
        if randint(1, 5) == 1:
            efeito_digitando("Monstros encontrados.")
            sleep(1)
            tela.limpar_tela()
            for y in range(randint(1, 3)):
                Inimigo = choice(monstros_da_floresta)
                inimigo = Inimigo(level=self.level)
                combate(self.personagem, inimigo)
                if self.personagem.morto():
                    return True
                else:
                    self.personagem.experiencia.depositar_valor(
                        inimigo.experiencia
                    )
                    inimigo.sortear_drops(self.personagem)
                    inimigo.sortear_drops_quest(self.personagem)
                self.personagem.recuperar_magia_stamina_cem_porcento()
            return False

    def morto(self):
        """Método que ressucita o personagem e exibe na tela "morto"."""
        self.personagem.ressucitar()
        tela.imprimir("você está morto e foi ressucitado.")
        sleep(3)
        tela.limpar_tela()

    def sortear_drop_quest_mapa(self):
        quests = filter(
            lambda quest: quest.tipo == "mapa", self.personagem.quests
        )
        for quest in quests:
            condicoes = [
                quest.sorte_de_drop(),
                (
                    self.personagem.inventario.count(quest.item)
                    < quest.numero_de_itens_requeridos
                ),
            ]
            if all(condicoes):
                if self.personagem.e_possivel_guardar(quest.item):
                    self.personagem.guardar_item(quest.item)
                    tela.imprimir(f"item {quest.item.nome} adiquirido.\n")
                    sleep(1)
                else:
                    tela.imprimir(
                        "não foi possível adicionar item ao inventario, "
                        "inventario cheio.\n"
                    )
                    sleep(3)

    def _sortear_boss_dragao(self):
        if randint(1, 25) == 25:
            status = {
                "vida": 300,
                "dano": 5,
                "resistencia": 15,
                "velo-ataque": 1,
                "critico": 15,
                "armadura": 15,
                "magia": 100,
                "stamina": 100,
                "velo-movi": 1,
            }
            boss = Dragao(self.level + 1, status)
            tela.limpar_tela()
            tela.imprimir("Dragão encontrado!\n", "vermelho")
            tela.imprimir(str(boss) + "\n")
            lutar = self._lutar_ou_fugir()
            if lutar:
                combate(self.personagem, boss)
                if not self.personagem.morto():
                    boss.sortear_drops(self.personagem)
                    boss.sortear_drops_quest(self.personagem)
            else:
                tela.imprimir("Dragão foi embora.\n", "vermelho")
                sleep(2)
                tela.limpar_tela()
            if self.personagem.morto():
                return "morto"

    def _lutar_ou_fugir(self):
        # esse método não limpa a tela, favor manter.
        tela.imprimir("Deseja lutar ou fugir?: ")
        resposta = tela.obter_string().lower()
        if resposta == "lutar":
            return True
        else:
            return False
