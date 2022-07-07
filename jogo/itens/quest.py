class ItemQuest:
    def __init__(self, nome):
        self.nome = nome
        self.tipo = "quest"
        self.classe = "quest"

    def __repr__(self):
        return f"Item de quest: {self.nome}"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.nome == other.nome:
            return True
        else:
            return False
