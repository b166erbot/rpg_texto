from unittest import TestCase

from jogo.utils import Acumulador


class TestAcumulador(TestCase):
    def setUp(self):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 1)

    def test_depositar_valor_retorna_level_3_caso_receba_3_de_valor(self):
        self.acumulador.depositar_valor(3)
        self.assertEqual(self.acumulador.level, 3)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_retorna_1_caso_receba_4_de_valor(self):
        self.acumulador.depositar_valor(4)
        self.assertEqual(self.acumulador.level, 3)
        self.assertEqual(int(self.acumulador), 1)

    def test_depositar_valor_retorna_level_maximo_caso_receba_21_de_valor(self):
        self.acumulador.depositar_valor(21)
        self.assertEqual(self.acumulador.level, 7)
        self.assertEqual(int(self.acumulador), 0)

    def test_depositar_valor_retorna_valor_0_caso_receba_22_de_valor(self):
        self.acumulador.depositar_valor(22)
        self.assertEqual(self.acumulador.level, 7)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_total_retorna_10_caso_level_seja_4(self):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 4)
        # 1 + 2 + 3 == 6
        self.assertEqual(self.acumulador.valor_total(), 6)

    def test_valor_total_retorna_21_caso_level_seja_7(self):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 7)
        self.assertEqual(self.acumulador.valor_total(), 21)

    def test_valor_retorna_0_caso_level_seja_7_e_valor_seja_1(self):
        self.acumulador = Acumulador(1, [1, 2, 3, 4, 5, 6], 7)
        self.assertEqual(self.acumulador.valor_total(), 21)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_total_retorna_21_caso_level_ultrapasse_o_limite_8(self):
        self.acumulador = Acumulador(1, [1, 2, 3, 4, 5, 6], 8)
        self.assertEqual(self.acumulador.valor_total(), 21)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_total_retorna_10_caso_depositar_valor_receba_10(self):
        self.acumulador.depositar_valor(10)
        self.assertEqual(self.acumulador.valor_total(), 10)

    def test_valor_total_retorna_11_caso_depositar_valor_receba_11(self):
        self.acumulador.depositar_valor(11)
        self.assertEqual(self.acumulador.valor_total(), 11)

    def test_valor_total_retorna_0_caso_acumular_level_8_e_depositar_valor_receba_10(
        self,
    ):
        self.acumulador = Acumulador(1, [1, 2, 3, 4, 5, 6], 8)
        self.acumulador.depositar_valor(10)
        self.assertEqual(self.acumulador.valor_total(), 21)
