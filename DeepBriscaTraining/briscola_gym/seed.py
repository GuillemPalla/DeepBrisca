from typing import Union
import numpy as np


class Seed:
    Oros = 1
    Copes = 2
    Espases = 3
    Bastos = 4
    __ohe = np.eye(4)

    @classmethod
    def get_seed(cls, i: Union[str, int]):
        assert 0 <= i <= 3, i
        if isinstance(i, str):
            return cls.__dict__[i.capitalize()]
        if i == 0:
            return cls.Oros
        elif i == 1:
            return cls.Copes
        elif i == 2:
            return cls.Espases
        elif i == 3:
            return cls.Bastos
        else:
            raise ValueError(f"input {i} should be between [0, 3]")

    @classmethod
    def get_name_seed(cls, i):
        assert 1 <= i <= 4, i
        if i == 1:
            return "Oros"
        elif i == 2:
            return "Copes"
        elif i == 3:
            return "Espases"
        elif i == 4:
            return "Bastos"
        else:
            raise ValueError(f"input {i} should be between [1, 4]")

    @classmethod
    def ohe_repr(cls, seed):
        return cls.__ohe[seed - 1, :]
