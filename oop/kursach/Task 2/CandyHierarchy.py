class Sweet:
    """
    Basic parent class for all types of sweets.
    """
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


class Candy(Sweet):
    def __init__(self, name: str, weight: float, flavor: str):
        super().__init__(name, weight)
        self._flavor = flavor

    @property
    def flavor(self) -> str:
        return self._flavor

    def __str__(self):
        return "Леденцовая конфета {}, вкус {}, {} г.".format(self._name, self._flavor, self._weight)


class Chocolate(Sweet):
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


class CandyOnStick(Candy):
    def __init__(self, name: str, weight: float, flavor: str, form: str):
        super().__init__(name, weight, flavor)
        self._form = form

    @property
    def form(self) -> str:
        return self._form

    def __str__(self):
        return "Леденец на палочке {}, вкус {}, форма {}, {} г.".format(self._name, self._flavor, self._form,
                                                                        self._weight)


class CandyInWrapper(Candy):
    def __init__(self, name: str, weight: float, flavor: str, wrapper_type: str):
        super().__init__(name, weight, flavor)
        self._wrapper_type = wrapper_type

    @property
    def wrapper_type(self) -> str:
        return self._wrapper_type

    def __str__(self):
        return "Леденец в обертке {}, вкус {}, обертка {}, {} г.".format(self._name, self._flavor, self._wrapper_type,
                                                                         self._weight)


class Gift:
    """
    A class that manages candy objects.
    """
    def __init__(self, recipient: str):
        self._sweets = []
        self._recipient = recipient

    def add_sweets(self, *sweets):
        for sweet in sweets:
            if isinstance(sweet, Sweet):
                self._sweets.append(sweet)
            else:
                print('Traceback: Error in Gift.add_sweets: Given objects must be objects of class Sweet')
        return self

    @property
    def weight(self):
        return sum(sweet.weight for sweet in self._sweets)

    def __str__(self):
        return "\n".join(str(sweet) for sweet in self._sweets)
