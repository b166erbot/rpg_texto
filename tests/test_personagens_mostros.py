import curses

curses.initscr()

from unittest import TestCase, mock
from unittest.mock import MagicMock

from jogo.itens.armas import (
    Adaga,
    AdornoDeArma,
    Arco_curto,
    Arco_longo,
    Botas_de_ferro,
    Cajado,
    Cajado_negro,
    Espada_curta,
    Espada_longa,
    Luvas_de_ferro,
    Machado,
)
from jogo.itens.caixas import CaixaDraconica
from jogo.itens.item_secundario import Adaga as AdagaSecundaria
from jogo.itens.item_secundario import (
    Aljava,
    BolaDeCristal,
    Buckler,
    Escudo,
    Livro,
)
from jogo.itens.quest import ItemQuest
from jogo.itens.vestes import Amuleto, Anel, Botas, Calca, Elmo, Luvas, Peitoral
from jogo.personagens.classes import Arqueiro
from jogo.personagens.monstros import (
    ArvoreDeku,
    Camaleao,
    Dragao,
    Mico,
    Sapo,
    Sucuri,
    Tamandua,
    Tartaruga,
    Topera,
)

curses.endwin()


# só precisa de um monstro para testar o método da classe Monstro
@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestMonstroDropandoItensCorretamenteItensSecundarios(TestCase):
    def setUp(self):
        self.monstro = Tartaruga()
        self.personagem = Arqueiro("nome", True)

    def test_sortear_drops_retorna_adaga_secundaria(self, randint, choice, *_):
        choice.return_value = AdagaSecundaria
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], AdagaSecundaria)

    def test_sortear_drops_retorna_livro(self, randint, choice, *_):
        choice.return_value = Livro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Livro)

    def test_sortear_drops_retorna_aljava(self, randint, choice, *_):
        choice.return_value = Aljava
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Aljava)

    def test_sortear_drops_retorna_bola_de_cristal(self, randint, choice, *_):
        choice.return_value = BolaDeCristal
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], BolaDeCristal)

    def test_sortear_drops_retorna_buckler(self, randint, choice, *_):
        choice.return_value = Buckler
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Buckler)

    def test_sortear_drops_retorna_escudo(self, randint, choice, *_):
        choice.return_value = Escudo
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Escudo)


@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestMonstroDropandoItensCorretamenteItensPrincipais(TestCase):
    def setUp(self):
        self.monstro = Tartaruga()
        self.personagem = Arqueiro("nome", True)

    def test_sortear_drops_retorna_adaga(self, randint, choice, *_):
        choice.return_value = Adaga
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Adaga)

    def test_sortear_drops_retorna_arco_curto(self, randint, choice, *_):
        choice.return_value = Arco_curto
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Arco_curto)

    def test_sortear_drops_retorna_arco_longo(self, randint, choice, *_):
        choice.return_value = Arco_longo
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Arco_longo)

    def test_sortear_drops_retorna_botas_de_ferro(self, randint, choice, *_):
        choice.return_value = Botas_de_ferro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Botas_de_ferro)

    def test_sortear_drops_retorna_cajado(self, randint, choice, *_):
        choice.return_value = Cajado
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Cajado)

    def test_sortear_drops_retorna_cajado_negro(self, randint, choice, *_):
        choice.return_value = Cajado_negro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Cajado_negro)

    def test_sortear_drops_retorna_espada_curta(self, randint, choice, *_):
        choice.return_value = Espada_curta
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Espada_curta)

    def test_sortear_drops_retorna_espada_longa(self, randint, choice, *_):
        choice.return_value = Espada_longa
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Espada_longa)

    def test_sortear_drops_retorna_luvas_de_ferro(self, randint, choice, *_):
        choice.return_value = Luvas_de_ferro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Luvas_de_ferro)

    def test_sortear_drops_retorna_machado(self, randint, choice, *_):
        choice.return_value = Machado
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Machado)

    def test_sortear_drops_retorna_adorno_de_arma(self, randint, choice, *_):
        choice.return_value = AdornoDeArma
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], AdornoDeArma)


@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestMonstroDropandoItensCorretamenteItensVestes(TestCase):
    def setUp(self):
        self.monstro = Tartaruga()
        self.personagem = Arqueiro("nome", True)

    def test_sortear_drops_retorna_elmo(self, randint, choice, *_):
        choice.return_value = Elmo
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Elmo)

    def test_sortear_drops_retorna_amuleto(self, randint, choice, *_):
        choice.return_value = Amuleto
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Amuleto)

    def test_sortear_drops_retorna_anel(self, randint, choice, *_):
        choice.return_value = Anel
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Anel)

    def test_sortear_drops_retorna_botas(self, randint, choice, *_):
        choice.return_value = Botas
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Botas)

    def test_sortear_drops_retorna_calca(self, randint, choice, *_):
        choice.return_value = Calca
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Calca)

    def test_sortear_drops_retorna_luvas(self, randint, choice, *_):
        choice.return_value = Luvas
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Luvas)

    def test_sortear_drops_retorna_peitoral(self, randint, choice, *_):
        choice.return_value = Peitoral
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Peitoral)


@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.sleep2")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestMonstroSortearDropsTestsAvulsos(TestCase):
    def setUp(self):
        self.monstro = Tartaruga()
        self.personagem = Arqueiro("nome", True)
        for _ in range(30):
            self.personagem.inventario.append(
                Elmo(vida=5, armadura=5, resistencia=5)
            )
        self.mock = MagicMock()
        self.personagem.guardar_item = self.mock

    def test_item_nao_e_guardado_caso_o_inventario_do_personagem_estiver_cheio(
        self, randint, choice, *_
    ):
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        self.mock.assert_not_called()

    def test_item_e_guardado_caso_o_inventario_do_personagem_nao_estiver_cheio(
        self, randint, choice, *_
    ):
        self.personagem.inventario.pop()
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        self.mock.assert_called()

    def test_randint_e_chamado_dando_pratas_ao_personagem(
        self, randint, choice, *_
    ):
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        randint.assert_called_with(30, 50)


class TestCriticoTartaruga(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_investida(self, mocked):
        self.monstro.investida(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 92)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_garras_afiadas(self, mocked):
        self.monstro.garras_afiadas(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 88)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_investida(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.investida(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 96)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_garras_afiadas(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.garras_afiadas(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 94)


class TestCriticoCamaleao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Camaleao()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_trapasseiro(self, mocked):
        self.monstro.trapasseiro(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 92)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_roubo(self, mocked):
        self.monstro.roubo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 88)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_trapasseiro(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.trapasseiro(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 96)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_roubo(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.roubo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 94)


class TestCriticoTamandua(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tamandua()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_linguada(self, mocked):
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 92)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_abraco(self, mocked):
        self.monstro.abraco(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 88)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_linguada(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 96)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_abraco(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.abraco(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 94)


class TestCriticoSapo(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sapo()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_linguada(self, mocked):
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 92)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_salto(self, mocked):
        self.monstro.salto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 88)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_linguada(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 96)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_salto(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.salto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 94)


# só precisa de um monstro boss para testar o método da classe Boss
@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestBossDropandoItensCorretamenteItensSecundarios(TestCase):
    def setUp(self):
        self.monstro = Topera()
        self.personagem = Arqueiro("nome", True)

    def test_sortear_drops_retorna_adaga_secundaria(self, randint, choice, *_):
        choice.return_value = AdagaSecundaria
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], AdagaSecundaria)

    def test_sortear_drops_retorna_livro(self, randint, choice, *_):
        choice.return_value = Livro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Livro)

    def test_sortear_drops_retorna_aljava(self, randint, choice, *_):
        choice.return_value = Aljava
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Aljava)

    def test_sortear_drops_retorna_bola_de_cristal(self, randint, choice, *_):
        choice.return_value = BolaDeCristal
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], BolaDeCristal)

    def test_sortear_drops_retorna_buckler(self, randint, choice, *_):
        choice.return_value = Buckler
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Buckler)

    def test_sortear_drops_retorna_escudo(self, randint, choice, *_):
        choice.return_value = Escudo
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Escudo)


@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestBossDropandoItensCorretamenteItensPrincipais(TestCase):
    def setUp(self):
        self.monstro = Topera()
        self.personagem = Arqueiro("nome", True)

    def test_sortear_drops_retorna_adaga(self, randint, choice, *_):
        choice.return_value = Adaga
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Adaga)

    def test_sortear_drops_retorna_arco_curto(self, randint, choice, *_):
        choice.return_value = Arco_curto
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Arco_curto)

    def test_sortear_drops_retorna_arco_longo(self, randint, choice, *_):
        choice.return_value = Arco_longo
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Arco_longo)

    def test_sortear_drops_retorna_botas_de_ferro(self, randint, choice, *_):
        choice.return_value = Botas_de_ferro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Botas_de_ferro)

    def test_sortear_drops_retorna_cajado(self, randint, choice, *_):
        choice.return_value = Cajado
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Cajado)

    def test_sortear_drops_retorna_cajado_negro(self, randint, choice, *_):
        choice.return_value = Cajado_negro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Cajado_negro)

    def test_sortear_drops_retorna_espada_curta(self, randint, choice, *_):
        choice.return_value = Espada_curta
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Espada_curta)

    def test_sortear_drops_retorna_espada_longa(self, randint, choice, *_):
        choice.return_value = Espada_longa
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Espada_longa)

    def test_sortear_drops_retorna_luvas_de_ferro(self, randint, choice, *_):
        choice.return_value = Luvas_de_ferro
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Luvas_de_ferro)

    def test_sortear_drops_retorna_machado(self, randint, choice, *_):
        choice.return_value = Machado
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Machado)

    def test_sortear_drops_retorna_adorno_de_arma(self, randint, choice, *_):
        choice.return_value = AdornoDeArma
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], AdornoDeArma)


@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestBossDropandoItensCorretamenteItensVestes(TestCase):
    def setUp(self):
        self.monstro = Topera()
        self.personagem = Arqueiro("nome", True)

    def test_sortear_drops_retorna_elmo(self, randint, choice, *_):
        choice.return_value = Elmo
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Elmo)

    def test_sortear_drops_retorna_amuleto(self, randint, choice, *_):
        choice.return_value = Amuleto
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Amuleto)

    def test_sortear_drops_retorna_anel(self, randint, choice, *_):
        choice.return_value = Anel
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Anel)

    def test_sortear_drops_retorna_botas(self, randint, choice, *_):
        choice.return_value = Botas
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Botas)

    def test_sortear_drops_retorna_calca(self, randint, choice, *_):
        choice.return_value = Calca
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Calca)

    def test_sortear_drops_retorna_luvas(self, randint, choice, *_):
        choice.return_value = Luvas
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Luvas)

    def test_sortear_drops_retorna_peitoral(self, randint, choice, *_):
        choice.return_value = Peitoral
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[0], Peitoral)


@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.sleep2")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestBossSortearDropsTestsAvulsos(TestCase):
    def setUp(self):
        self.monstro = Topera()
        self.personagem = Arqueiro("nome", True)
        for _ in range(30):
            self.personagem.inventario.append(
                Elmo(vida=5, armadura=5, resistencia=5)
            )
        self.mock = MagicMock()
        self.personagem.guardar_item = self.mock

    def test_item_nao_e_guardado_caso_o_inventario_do_personagem_estiver_cheio(
        self, randint, choice, *_
    ):
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        self.mock.assert_not_called()

    def test_item_e_guardado_caso_o_inventario_do_personagem_nao_estiver_cheio(
        self, randint, choice, *_
    ):
        self.personagem.inventario.pop()
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        self.mock.assert_called()

    def test_randint_e_chamado_dando_pratas_ao_personagem(
        self, randint, choice, *_
    ):
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        randint.assert_called_with(60, 100)


class TestCriticoTopera(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Topera()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_pulo_fatal(self, mocked):
        self.monstro.pulo_fatal(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_terremoto(self, mocked):
        self.monstro.terremoto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_pulo_fatal(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.pulo_fatal(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_terremoto(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.terremoto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoMico(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Mico()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_tacar_banana(self, mocked):
        self.monstro.tacar_banana(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_esmagar(self, mocked):
        self.monstro.esmagar(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_tacar_banana(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.tacar_banana(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_esmagar(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.esmagar(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoSucuri(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sucuri()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_lancamento_de_calda(self, mocked):
        self.monstro.lancamento_de_calda(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_bote(self, mocked):
        self.monstro.bote(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_lancamento_de_calda(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.lancamento_de_calda(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_bote(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.bote(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoArvoreDeku(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = ArvoreDeku()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_braçada(self, mocked):
        self.monstro.braçada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_outono(self, mocked):
        self.monstro.outono(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_braçada(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.braçada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_outono(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.outono(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoDragao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Dragao()
        self.monstro.porcentagem_critico = 100

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_patada(self, mocked):
        self.monstro.patada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_critico_em_personagem_fogo(self, mocked):
        self.monstro.fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_patada(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.patada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.monstros.randint", return_value=100)
    def test_sem_critico_em_personagem_fogo(self, mocked):
        self.monstro.porcentagem_critico = 0
        self.monstro.fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


@mock.patch("jogo.personagens.monstros.tela")
@mock.patch("jogo.personagens.monstros.sleep2")
@mock.patch("jogo.personagens.monstros.efeito_digitando")
@mock.patch("jogo.personagens.monstros.choice", return_value=MagicMock())
@mock.patch("jogo.personagens.monstros.randint", return_value=1)
class TestDragaoDropandoItens(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Dragao()

    def test_monstro_dropando_item_quest_coracao(self, randint, choice, *_):
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        item = ItemQuest("Coração de Dragão")
        self.assertIn(item, self.personagem.inventario)

    def test_monstro_dopando_caixa_draconica(self, randint, choice, *_):
        choice.return_value = MagicMock(tipo="Arma")
        self.monstro.sortear_drops(self.personagem)
        self.assertIsInstance(self.personagem.inventario[2], CaixaDraconica)


class TestPorcentagemArmaduraResistenciaTartaruga(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaCamaleao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Camaleao()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaTamandua(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tamandua()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaSapo(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sapo()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaTopera(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Topera()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaMico(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Mico()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaSucuri(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sucuri()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaArvoreDeku(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = ArvoreDeku()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


class TestPorcentagemArmaduraResistenciaDragao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Dragao()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80

    def test_monstro_recebe_80_porcento_a_menos_de_dano_armadura(self):
        self.personagem.tres_flechas(self.monstro)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_monstro_recebe_80_porcento_a_menos_de_dano_resistencia(self):
        self.personagem.flecha_de_fogo(self.monstro)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.monstro.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoTartaruga(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tartaruga()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_investida(
        self, *_
    ):
        dano = 4
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.investida(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_garras_afiadas(
        self, *_
    ):
        dano = 6
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.garras_afiadas(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoCamaleao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Camaleao()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_trapasseiro(
        self, *_
    ):
        dano = 4
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.trapasseiro(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_roubo(self, *_):
        dano = 6
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.roubo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoTamandua(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tamandua()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_linguada(self, *_):
        dano = 4
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_abraco(self, *_):
        dano = 6
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.abraco(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoSapo(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sapo()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_linguada(self, *_):
        dano = 4
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_salto(self, *_):
        dano = 6
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.salto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoTopera(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Topera()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_pulo_fatal(
        self, *_
    ):
        dano = 10
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.pulo_fatal(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_terremoto(
        self, *_
    ):
        dano = 15
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.terremoto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoMico(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Mico()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_tacar_banana(
        self, *_
    ):
        dano = 10
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.tacar_banana(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_esmagar(self, *_):
        dano = 15
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.esmagar(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoSucuri(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sucuri()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_lancamento_de_calda(
        self, *_
    ):
        dano = 10
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.lancamento_de_calda(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_bote(self, *_):
        dano = 15
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.bote(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoArvoreDeku(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = ArvoreDeku()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_braçada(self, *_):
        dano = 10
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.braçada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_outono(self, *_):
        dano = 15
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.outono(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioDandoMenosDanoDragao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Dragao()
        self.personagem.porcentagem_armadura = 0
        self.personagem.porcentagem_resistencia = 0
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_patada(self, *_):
        dano = 10
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.patada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_fogo(self, *_):
        dano = 15
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoTartaruga(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tartaruga()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_investida(
        self, *_
    ):
        dano = 4
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.investida(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_garras_afiadas(
        self, *_
    ):
        dano = 6
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.garras_afiadas(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoCamaleao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Camaleao()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_trapasseiro(
        self, *_
    ):
        dano = 4
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.trapasseiro(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_roubo(self, *_):
        dano = 6
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.roubo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoTamandua(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Tamandua()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_linguada(self, *_):
        dano = 4
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_abraco(self, *_):
        dano = 6
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.abraco(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoSapo(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sapo()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_linguada(self, *_):
        dano = 4
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.linguada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_salto(self, *_):
        dano = 6
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.salto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoTopera(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Topera()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_pulo_fatal(
        self, *_
    ):
        dano = 10
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.pulo_fatal(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_terremoto(
        self, *_
    ):
        dano = 15
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.terremoto(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoMico(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Mico()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_tacar_banana(
        self, *_
    ):
        dano = 10
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.tacar_banana(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_esmagar(self, *_):
        dano = 15
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.esmagar(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoSucuri(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Sucuri()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_lancamento_de_calda(
        self, *_
    ):
        dano = 10
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.lancamento_de_calda(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_bote(self, *_):
        dano = 15
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.bote(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoArvoreDeku(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = ArvoreDeku()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_braçada(self, *_):
        dano = 10
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.braçada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_outono(self, *_):
        dano = 15
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.outono(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)


@mock.patch("jogo.personagens.monstros.randint", return_value=100)
class TestBloqueioArmaduraResistenciaDandoMenosDanoDragao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.monstro = Dragao()
        self.personagem.porcentagem_armadura = 80
        self.personagem.porcentagem_resistencia = 80
        self.personagem.valor_de_bloqueio = 0.80
        self.monstro.porcentagem_critico = 0

    def test_personagem_deve_receber_menos_dano_com_bloqueio_patada(self, *_):
        dano = 10
        # primeiro o dano é redusido a armadura/resistencia
        dano = dano - int((dano * 80) // 100)
        # vida do monstro - (dano do personagem - porcentagem do bloqueio)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.patada(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem_deve_receber_menos_dano_com_bloqueio_fogo(self, *_):
        dano = 15
        dano = dano - int((dano * 80) // 100)
        esperado = 100 - (dano - (dano * self.personagem.valor_de_bloqueio))
        self.monstro.fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], esperado)
