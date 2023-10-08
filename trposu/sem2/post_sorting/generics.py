class Office:
    def __new__(cls, id_, number):
        number = str(number)
        assert number, 'Укажите номер отделения'
        assert number.isdigit(), 'Номер отделения должен состоять из цифр'
        assert len(number) == 4, 'Номер отделения должен состоять из 4 символов'
        return super(Office, cls).__new__(cls)

    def __init__(self, id_: int, number: str):
        self.id = int(id_)
        self.number = str(number)

    def __str__(self):
        return self.number


class Street:
    def __new__(cls, id_, name, office):
        name = str(name)
        assert name, 'Укажите название улицы'
        assert type(office) == Office, 'Улица должна содержать ссылку на отделение'
        assert len(name) >= 1, 'Название улицы не может быть короче 1 символа'
        assert len(name) <= 40, 'Название улицы не может быть длиннее 40 символов'
        return super(Street, cls).__new__(cls)

    def __init__(self, id_: int, name: str, office: Office):
        self.id = int(id_)
        self.name = str(name)
        self.office = office

    def __str__(self):
        return self.name + ' ул.'


class Parcel:
    def __new__(cls, id_, office, street, type_):
        assert type(office) == Office, 'Посылка должна содержать ссылку на отделение'
        assert type(street) == Street, 'Посылка должна содержать ссылку на улицу'
        if type_:
            type_ = int(type_)
            assert 1 <= type_ <= 3, 'Тип посылки должен быть целым числом от 1 до 3'
        return super(Parcel, cls).__new__(cls)

    def __init__(self, id_: int, office: Office, street: Street, type_: int = None):
        self.id = int(id_)
        self.office = office
        self.street = street
        self.type = int(type_) if type_ else None

    @property
    def type_str(self):
        types = {1: 'Большая', 2: 'Средняя', 3: 'Маленькая'}
        return types.get(self.type, '')

    def __str__(self):
        if self.type_str:
            parcel_type = self.type_str + ' посылка'
        else:
            parcel_type = 'Посылка'
        return '{} №{}, ({}, отделение №{})'.format(parcel_type, self.id, self.street, self.office.number)


class User:
    def __init__(self, id_: int, username: str, password: str, permissions: int):
        self.id = int(id_)
        self.username = str(username)
        self.password = str(password)
        self.permissions = int(permissions)

    def __str__(self):
        return self.username
