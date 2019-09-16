from unittest import TestCase
from unittest.mock import MagicMock
from jogo.personagens.classes import (
    Humano, Arqueiro, Guerreiro, Mago, Assassino, Clerigo
)


class TestesHumanoAtacar(TestCase):
    def setUp(self):
        self.func = Humano.atacar
        self.args = (MagicMock(), MagicMock(), MagicMock())
        self.args[0].jogador = 'bot'

    def test_atacar_chamando_atacar_como_bot(self):
        self.func(*self.args)
        vezes_chamado = self.args[0]._atacar_como_bot.call_count
        self.assertEqual(vezes_chamado, 1)

    def test_atacar_chamando_atacar_como_jogador(self):
        self.args[0].jogador = 'humano'
        self.func(*self.args)
        vezes_chamado = self.args[0]._atacar_como_jogador.call_count
        self.assertEqual(vezes_chamado, 1)


class TestesHumanoRessucitar(TestCase):
    def setUp(self):
        self.func = Humano.ressucitar
        self.args = (MagicMock(),)
        self.args[0].status = {'vida': 0}

    def test_ressucitar_retornando_toda_a_vida(self):
        self.func(*self.args)
        self.assertEqual(self.args[0].status['vida'], 100)


class TestesAssassinoAtacar(TestesHumanoAtacar):
    def setUp(self):
        super().setUp()
        self.func = Assassino.atacar


class TestesAssassinoRessucitar(TestesHumanoRessucitar):
    def setUp(self):
        super().setUp()
        self.func = Assassino.ressucitar

class TestesGuerreiroAtacar(TestesHumanoAtacar):
    def setUp(self):
        super().setUp()
        self.func = Guerreiro.atacar


class TestesGuerreiroRessucitar(TestesHumanoRessucitar):
    def setUp(self):
        super().setUp()
        self.func = Guerreiro.ressucitar

class TestesMagoAtacar(TestesHumanoAtacar):
    def setUp(self):
        super().setUp()
        self.func = Mago.atacar


class TestesMagoRessucitar(TestesHumanoRessucitar):
    def setUp(self):
        super().setUp()
        self.func = Mago.ressucitar

class TestesArqueiroAtacar(TestesHumanoAtacar):
    def setUp(self):
        super().setUp()
        self.func = Arqueiro.atacar


class TestesArqueiroRessucitar(TestesHumanoRessucitar):
    def setUp(self):
        super().setUp()
        self.func = Arqueiro.ressucitar

class TestesClerigoAtacar(TestesHumanoAtacar):
    def setUp(self):
        super().setUp()
        self.func = Clerigo.atacar


class TestesClerigoRessucitar(TestesHumanoRessucitar):
    def setUp(self):
        super().setUp()
        self.func = Clerigo.ressucitar
