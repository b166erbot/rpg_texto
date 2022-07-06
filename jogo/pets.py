class Pet:
    def __init__(self, nome: str, atributo: str, valor: int):
        self.nome = nome
        self.atributo = atributo
        self.valor = valor
        self.classe = 'Pet'
        self.tipo = "Pet"
    
    def __repr__(self):
        retorno = (
            f"pet({self.nome}, atributo: {self.atributo}, "
            f"valor: {self.valor}%)"
        )
        return retorno

    def calcular_bonus(self, personagem):
        valor = personagem.status[self.atributo]
        adicionar_valor = (valor * self.valor) // 100
        personagem.status[self.atributo] += adicionar_valor


class SemPet:
    def __init__(self):
        self.nome = "Sem pet"
        self.classe = 'Pet'
        self.tipo = "Pet"

    def __repr__(self):
        return "sem pet"

    def calcular_bonus(self, personagem):
        pass
