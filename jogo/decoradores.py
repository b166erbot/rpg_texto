from typing import Callable


def validador(funcao: Callable, Excecao: Exception, texto: str):
    """ Decorador que valida os argumentos com base na função passada. """
    def obter_funcao(func):
        def obter_argumentos(*argumentos):
            if funcao(argumentos):  # len(argumentos) != quantidade:
                raise Excecao(texto)
            return func(*argumentos)
        return obter_argumentos
    return obter_funcao
