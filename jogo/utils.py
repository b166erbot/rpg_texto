import pickle


def salvar_jogo(objeto, nome_do_arquivo):
    with open(nome_do_arquivo, 'wb') as arquivo:
        pickle.dump(objeto, arquivo, pickle.HIGHEST_PROTOCOL)


def carregar_jogo(nome_do_arquivo):
    with open(nome_do_arquivo, 'rb') as arquivo:
        return pickle.load(arquivo)


def chunk(lista, numero):
    return [lista[x:x + numero] for x in range(0, len(lista), numero)]


class Substantivo:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return 'a' if self.nome.endswith('a') else 'o'
