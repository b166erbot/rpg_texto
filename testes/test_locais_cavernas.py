# from unittest import TestCase
# from unittest.mock import MagicMock
# from jogo.locais.cavernas import *
# from typing import Generator
#
#
# dicio = {
#     'bifurcação': {
#         'caminho1': {
#             'bifurcação': {
#                 'caminho1': 'estreito e sem saída',
#                 'caminho2': {
#                     'outra passagem': {
#                         'caminho1': {
#                             'outra passagem': {
#                                 'caminho1': 'mineiração',
#                                 'caminho2': 'cachoeira interna'
#                             }
#                         },
#                         'caminho2': {
#                             'outra passagem': {
#                                 'caminho1': 'estreito e sem saída',
#                                 'caminho2': 'mineiração'
#                             }
#                         }
#                     }
#                 }
#             }
#         },
#         'caminho2': {
#             'bifurcação': {
#                 'caminho1': 'mineiração',
#                 'caminho2': {
#                     'outra passagem': {
#                         'caminho1': 'mineiração',
#                         'caminho2': 'sem saída'
#                     }
#                 }
#             }
#         }
#     }
# }
#
#
# class TestesCavernaMetodoOrganizarRotas(TestCase):
#     def setUp(self):
#         self.func = Caverna.organizar_rotas
#         self.args = (MagicMock(), dicio)
#
#     def test_retornando_um_generator(self):
#         resultado = self.func(*self.args)
#         self.assertIsInstance(resultado, Generator)
#
#     def test_retornando_conteudo_na_ordem_esperada(self):
#         resultado = list(self.func(*self.args))
#         esperado = []
#         self.assertEqual(resultado, esperado)
