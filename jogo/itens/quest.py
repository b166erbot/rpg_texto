class ItemQuest:
    def __init__(self, nome):
        self.nome = nome
        self.tipo = "quest"

    def __repr__(self):
        return f"Item de quest: {self.nome}"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        condicoes = [
            self.nome == other.nome,
        ]
        if all(condicoes):
            return True
        else:
            return False
