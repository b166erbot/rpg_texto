import curses

curses.initscr()

from unittest import TestCase, mock

from jogo.itens.vestes import Peitoral
from jogo.personagens.classes import Arqueiro
from jogo.personagens.npc import Ferreiro

curses.endwin()


@mock.patch("jogo.personagens.npc.sleep")
@mock.patch("jogo.personagens.npc.tela")
class TestFerreiro(TestCase):
    def setUp(self):
        self.peitoral = Peitoral(vida=5, armadura=5, resistencia=5)
        self.ferreiro = Ferreiro("nome")
        self.personagem = Arqueiro("nome", True)
        self.personagem.inventario.append(self.peitoral)
        self.personagem.moedas["Glifos"] += 5000

    def test_personagem_derrete_item_no_inventario(self, tela, *_):
        tela.obter_string.side_effect = ["1", "0", "", ""]
        self.ferreiro.interagir(self.personagem)
        self.assertEqual(len(self.personagem.inventario), 0)
        self.assertEqual(int(self.personagem.moedas["Glifos"]), 5012)

    def test_acrescentar_glifos_aumenta_o_level_do_item_no_inventario(
        self, tela, *_
    ):
        tela.obter_string.side_effect = ["2", "0", "3600", "", ""]
        self.ferreiro.interagir(self.personagem)
        self.assertEqual(self.peitoral.level, 9)
        self.assertEqual(int(self.personagem.moedas["Glifos"]), 1400)

    def test_acrescentar_glifos_aumenta_o_level_do_item_equipado(
        self, tela, *_
    ):
        self.personagem.equipar(self.peitoral)
        tela.obter_string.side_effect = ["2", "0", "3600", "", ""]
        self.ferreiro.interagir(self.personagem)
        self.assertEqual(self.peitoral.level, 9)
        self.assertEqual(int(self.personagem.moedas["Glifos"]), 1400)

    def test_acrescentar_nao_aumenta_o_level_caso_quantidade_de_glifos_forem_maior_do_que_o_personagem_tem(
        self, tela, *_
    ):
        tela.obter_string.side_effect = ["2", "0", "5001", "", ""]
        self.ferreiro.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Glifos"]), 5000)
