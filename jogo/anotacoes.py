from typing import Union  # , TypeVar
from jogo.personagens.classes import (
    Arqueiro, Guerreiro, Mago, Assassino, Clerigo
)

Personagens = Union[Arqueiro, Guerreiro, Mago, Assassino, Clerigo]
