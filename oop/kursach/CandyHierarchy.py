class Sweet:  # конфета
    def __new__(cls, *args, **kwargs):
        return super(Sweet, cls).__new__(cls)

    def __init__(self, name: str, weight: float):
        self._name = name
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def __str__(self):
        return "Сладость {}, {} г.".format(self._name, self._weight)


class Candy(Sweet):  # сосулька
    def __init__(self, name: str, weight: float, flavor: str):
        super().__init__(name, weight)
        self._flavor = flavor

    @property
    def flavor(self) -> str:
        return self._flavor

    def __str__(self):
        return "Сладость {}, вкус {}, {} г.".format(self._name, self._flavor, self._weight)


class Chocolate(Sweet):  # шоколадная
    def __init__(self, name: str, weight: float, choco_type: str, cocoa_percent: float):
        super().__init__(name, weight)
        self._cocoa_percent = cocoa_percent
        self._choco_type = choco_type

    @property
    def cocoa_percent(self) -> float:
        return self._cocoa_percent

    def __str__(self):
        return 'Шоколад "{}" {}, какао {}%, {} г.'.format(self._name, self._choco_type, self._cocoa_percent,
                                                         self._weight)


class CandyOnStick(Candy):  # сосулька на палочке
    def __init__(self, name: str, weight: float, flavor: str, form: str):
        super().__init__(name, weight, flavor)
        self._form = form

    @property
    def form(self) -> str:
        return self._form

    def __str__(self):
        return "Сладость {}, вкус {}, форма {}, {} г.".format(self._name, self._flavor, self._form, self._weight)

class CandyInWrapper(Candy):  # сосулька в обертке
    def __init__(self, name: str, weight: float, flavor: str, wrapper_type: str):
        super().__init__(name, weight, flavor)
        self._wrapper_type = wrapper_type

    @property
    def wrapper_type(self) -> str:
        return self._wrapper_type

    def __str__(self):
        return "Сладость {}, вкус {}, обертка {}, {} г.".format(self._name, self._flavor, self._wrapper_type,
                                                                     self._weight)


class Gift:
    def __init__(self, recipient: str):
        self._sweets = []
        self._recipient = recipient

    def add_sweet(self, sweet):
        self._sweets.append(sweet)
        return self

    @property
    def weight(self):
        return sum(sweet.weight for sweet in self._sweets)

    def __str__(self):
        return "\n".join(f'{sweet_info}' for sweet_info in self._sweets)
