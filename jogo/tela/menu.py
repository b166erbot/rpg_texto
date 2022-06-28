import sys
from pathlib import Path
from time import sleep
from unittest.mock import MagicMock

from jogo.locais.areas_abertas import Floresta
from jogo.locais.habitaveis import Vilarejo
from jogo.quests import ItemQuest
from jogo.save import salvar_jogo
from jogo.tela.imprimir import Imprimir, formas
from jogo.utils import chunk

# Silenciar o pygame para não imprimir nada na tela
sys.stdout = MagicMock()
from pygame import mixer

sys.stdout = sys.__stdout__


mixer.init()
tela = Imprimir()


class Menu:
    def __init__(self, personagem, nome_jogo: str):
        self._nome_jogo = nome_jogo
        texto = ["O que deseja fazer?"]
        texto2 = [
            "explorar uma floresta",
            "visitar o vilarejo",
            "equipar equipamentos",
            "desequipar equipamentos",
            "mostrar equipamentos equipados",
            "vender itens",
            "mostrar o status",
            "mostrar quests",
            "salvar jogo",
            "deletar save",
            "sair",
        ]
        self._texto = texto + [
            f"{numero} - {texto}" for numero, texto in enumerate(texto2, 1)
        ]
        self.personagem = personagem

    def ciclo(self):
        """Método onde é exibido o menu principal para o usuário."""
        mixer.music.load("vilarejo.ogg")
        mixer.music.play()
        forma = f"{formas[227]} {{}} {formas[228]}"
        while True:
            tela.limpar_tela()
            for texto in self._texto:
                tela.imprimir(forma.format(texto) + "\n", "cyan")
            tela.imprimir(": ")
            caracter = tela.obter_string()
            if not caracter.isnumeric():
                continue
            caracter = int(caracter)
            match caracter:
                case 1:
                    mixer.music.stop()
                    continuar = self._primeira_vez()
                    if continuar:
                        self.floresta()
                    mixer.music.load("vilarejo.ogg")
                    mixer.music.play()
                case 2:
                    try:
                        npcs = getattr(self, "_npcs")
                    except AttributeError:
                        raise Exception(
                            'Você esqueceu de chamar o metodo "obter_npcs" '
                            "com a lista de npcs."
                        )
                    vilarejo = Vilarejo(
                        "Vila dos hobbits", self.personagem, npcs
                    )
                    vilarejo.explorar()
                case 3:
                    self.equipar_equipamentos()
                case 4:
                    self.desequipar()
                case 5:
                    tela.limpar_tela()
                    equipamentos = self.personagem.equipamentos.items()
                    for nome, item in equipamentos:
                        if bool(item):
                            frase = f"{nome}: {item}\n"
                        else:
                            frase = str(item) + "\n"
                        tela.imprimir(frase)
                    tela.imprimir(
                        "aperte enter para retornar ao menu principal: "
                    )
                    tela.obter_string()
                case 6:
                    self.vender_item()
                case 7:
                    tela.limpar_tela()
                    tela.imprimir(
                        self._arrumar_status(self.personagem),
                        "cyan",
                    )
                    tela.imprimir(
                        "aperte enter para retornar ao menu principal: ", "cyan"
                    )
                    tela.obter_string()
                case 8:
                    self._obter_numero_quests()
                case 9:
                    npcs = filter(lambda x: x.salvar, self._npcs)
                    salvar_jogo(self.personagem, npcs, self._nome_jogo)
                    tela.imprimir("jogo salvo", "cyan")
                    sleep(3)
                case 10:
                    tela.limpar_tela()
                    tela.imprimir(
                        "Tem certeza que deseja deletar o save? "
                        "[s/n/sim/não]: "
                    )
                    resposta = tela.obter_string()
                    if resposta in ["s", "sim"]:
                        arquivo = Path(self._nome_jogo)
                        if arquivo.exists():
                            arquivo.unlink()
                            tela.imprimir("save deletado", "cyan")
                        else:
                            tela.imprimir("save não existente", "cyan")
                        sleep(3)
                case 11:
                    quit()

    def equipar_equipamentos(self):
        """Método que equipa equipamentos do inventário do personagem."""
        equipamentos = list(
            filter(lambda x: x, self.personagem.equipamentos.values())
        )
        numero = self._obter_numero_equipamentos(
            "deseja equipar qual equipamento?: ",
            equipamentos + self.personagem.inventario,
        )
        if bool(numero):
            inventario = dict(
                enumerate(equipamentos + self.personagem.inventario)
            )
            equipamento = inventario.get(int(numero))
            if bool(equipamento) and equipamento in self.personagem.inventario:
                self.personagem.equipar(equipamento)

    def vender_item(self):
        """Método que vende um item do inventário do personagem."""
        numero = self._obter_numero_equipamentos(
            "deseja vender qual equipamento?: ", self.personagem.inventario
        )
        if bool(numero):
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                if not isinstance(equipamento, ItemQuest):
                    self.personagem.desequipar(equipamento)
                    self.personagem.vender(equipamento)

    def desequipar(self):
        """Método que desequipa um equipamento do personagem."""
        numero = self._obter_numero_equipamentos(
            "deseja desequipar qual equipamento?: ",
            list(self.personagem.equipamentos.values()),
        )
        if bool(numero):
            inventario = dict(enumerate(self.personagem.equipamentos.values()))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self.personagem.desequipar(equipamento)

    def floresta(self):
        """Método que conduz o personagem à floresta."""
        tela.limpar_tela()
        nomes_florestas = [
            "floresta rio preto",
            "floresta do caçador",
            "floresta mata grande",
            "floresta passo fundo",
            "floresta nublada",
            "floresta negra",
            "amazonia",
        ]
        nomes_florestas_dict = dict(enumerate(nomes_florestas, 1))
        for numero, floresta in enumerate(nomes_florestas, 1):
            tela.imprimir(
                f"{numero} - {floresta} [nível da floresta: {numero}]\n",
                "amarelo",
            )
        tela.imprimir(": ")
        numero = tela.obter_string()
        if numero.isnumeric() and int(numero) in nomes_florestas_dict:
            mixer.music.load("som_da_floresta.ogg")
            mixer.music.play()
            numero = int(numero)
            floresta = nomes_florestas_dict[int(numero)]
            floresta = Floresta(floresta, self.personagem, numero)
            floresta.explorar()
            self.personagem.recuperar_magia_stamina_cem_porcento()
            self.personagem.ressucitar()
            mixer.music.stop()

    def _obter_numero_equipamentos(self, mensagem: str, itens: list):
        """Método que organiza as páginas para o usuário e retorna um número."""
        itens = list(enumerate(itens))
        if len(itens) == 0:
            tela.imprimir("você não tem itens no inventario.", "cyan")
            sleep(2)
            return ""
        itens = chunk(itens, 17)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            tela.imprimir(
                "itens coloridos de amarelo estão equipados\n", "cyan"
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n - 1]:
                mensagem2 = (
                    f"{numero} - {item} [classe: {item.classe}]"
                    if item.tipo
                    in [
                        "Elmo",
                        "Peitoral",
                        "Calça",
                        "Botas",
                        "Luvas",
                        "Anel",
                        "Amuleto",
                        "Arma",
                        "Escudo",
                    ]
                    else f"{numero} - {item}"
                )
                equipamento_equipado = map(
                    lambda x: x is item, self.personagem.equipamentos.values()
                )
                if any(equipamento_equipado):
                    tela.imprimir(mensagem2 + "\n", "amarelo")
                else:
                    tela.imprimir(mensagem2 + "\n")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        return numero

    def _obter_numero_quests(self):
        quests = list(enumerate(self.personagem.quests))
        if len(quests) == 0:
            tela.imprimir("você não tem quests.", "cyan")
            sleep(2)
            return
        quests = chunk(quests, 17)
        numeros_paginas = {f":{n}": n for n in range(1, len(quests) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(quests)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in quests[n - 1]:
                tela.imprimir(f"{numero} - {item}\n")
            tela.imprimir("aperte enter para retornar ao menu: ", "cyan")
            numero = tela.obter_string()

    def obter_npcs(self, npcs: list):
        self._npcs = npcs

    def _primeira_vez(self):
        tela.limpar_tela()
        pocoes = list(
            filter(
                lambda x: x.nome in "poção de vida média",
                self.personagem.inventario,
            )
        )
        condicoes = [
            self.personagem.level == 1,
            int(self.personagem.experiencia) == 0,
            len(pocoes) < 10,
        ]
        if all(condicoes):
            tela.imprimir(
                "Como é a sua primeira vez, certifique-se de comprar de "
                "15 a 20 poções de vida média no comerciante do vilarejo.\n"
            )
            tela.imprimir("Deseja continuar mesmo assim?: ")
            caracter = tela.obter_string().lower()
            if caracter in ["s", "sim"]:
                return True
            else:
                return False
        return True

    def _arrumar_status(self, personagem):
        p = personagem
        armadura = f"armadura - {p.status['armadura']}"
        resistencia = f"resistencia - {p.status['resistencia']}"
        arm_porc = f"defesa da armadura % - {p.porcentagem_armadura}%"
        resi_porc = f"defesa da resistencia % - {p.porcentagem_resistencia}%"
        experiencia = f"xp - {p.experiencia}"
        pratas = f"{str(p.moedas['Pratas'])}"
        por_cri = f"porcentagem de dano critico - {p.porcentagem_critico}"
        critico = f"critico - {p.status['critico']}"
        aum_cri = f"aumento de dano critico % - {p.aumento_dano_critico}%\n"
        tamanhos = (
            len(x)
            for x in (
                armadura, resistencia, experiencia, pratas, critico,
                aum_cri
            )
        )
        len_max = max(tamanhos)
        textos = [
            f"{p.nome_completo[:67]} [{p.classe}]:",
            f"vida - {p.status['vida']}",
            f"{armadura: <{len_max}}{arm_porc}",
            f"{resistencia: <{len_max}}{resi_porc}",
            f"dano - {p.status['dano']}",
            f"{critico: <{len_max}}{por_cri}%",
            f"aumento de dano critico - {p.aumento_dano_critico}\n"
            f"{pratas: <{len_max}}{str(p.moedas['Draconica'])}",
            f"{experiencia: <{len_max}}level - {p.level}",
        ]
        return "\n".join(textos) + "\n"


# TODO: colocar mais npcs com quests.
# TODO: poções, venenos.
# TODO: combate entre personagens bots.
# TODO: colocar o nome dos ataques tanto dos inimigos tanto do personagem na tela.
# TODO: com o level, colocar subclasses aos personagens.
# TODO: fazer uma função que imprime a história do jogo.
# TODO: histórias tem botão de skip (não sei se tem como fazer)
# TODO: obsessão por primitivos na classe Humano (não tem como)
# TODO: adicionar quests que fazem os bosses dropar o item.
# TODO: elixir deve ter um preço diferente para cada level.
# TODO: level nos equipamentos, itens.
# TODO: implementar stun.
# TODO: interagir com cenários e destruílos?
# TODO: fazer quests onde o personagem precise interagir com 2 ou mais npcs.
# TODO: botar um simbolo diferente para a moeda draconica.
# TODO: fazer 10 poções ocuparem o mesmo espaço? (não sei se tem como)
# TODO: implementar deletar save no inicio
# TODO: implementar baús que dropam itens/draconica?
# TODO: ter um companheiro na campanha? (não sei se tem como implementar isso)
# TODO: trols, cavaleiros negros, catatumbas
# TODO: implementar chance de bloqueio do escudo