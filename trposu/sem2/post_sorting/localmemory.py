from db import Database
from generics import Office, Street, Parcel, User


class LocalMemory:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = Database(db_name)
        self.db.start()

        self.offices = None
        self.office_last_id = None
        self.streets = None
        self.street_last_id = None
        self.parcels = None
        self.parcel_last_id = None
        self._users = None

        self.parcels_info = {}
        self.is_changed = False
        self.authenticated_user = None

        self._load_data_from_db()

    def __del__(self):
        self.db.stop()

    def _load_data_from_db(self):
        data = self.db.get_data()

        # Offices
        self.offices = [Office(office[0], office[1]) for office in data[0]]
        self.office_last_id = self.offices[-1].id if self.offices else 0

        # Streets
        self.streets = []
        for street in data[1]:
            office = next(office_obj for office_obj in self.offices if street[2] == office_obj.id)
            self.streets.append(Street(street[0], street[1], office))
        self.street_last_id = self.streets[-1].id if self.streets else 0

        # Parcels
        self.parcels = []
        for parcel in data[2]:
            office = next(office_obj for office_obj in self.offices if parcel[1] == office_obj.id)
            street = next(street_obj for street_obj in self.streets if parcel[2] == street_obj.id)
            self.parcels.append(Parcel(parcel[0], office, street, parcel[3]))
        self.parcel_last_id = self.parcels[-1].id if self.parcels else 0

        # Users
        self._users = [User(user[0], user[1], user[2], user[3]) for user in data[3]]

        self._make_change()
        self.is_changed = False

    def _make_change(self):
        self.is_changed = True

        data = {}
        for parcel in self.parcels:
            data.setdefault(parcel.office, {
                '1': 0,
                '2': 0,
                '3': 0,
                'total': 0,
            })
            if parcel.type:
                data[parcel.office][str(parcel.type)] += 1
            data[parcel.office]['total'] += 1
        self.parcels_info = data

    def get_streets_by_office(self, office: Office):
        return [street for street in self.streets if street.office.id == office.id]

    def get_office_street_by_street_name(self, street_name: str):
        try:
            return next(street for street in self.streets if street.name == street_name)
        except StopIteration:
            return None

    def add_office(self, number: str):
        new_id = self.office_last_id + 1
        try:
            office = Office(new_id, number)
            self.offices.append(office)
            self.office_last_id = new_id
            self._make_change()
            return {'success': True, 'instance': office}
        except AssertionError as e:
            return {'success': False, 'message': e}

    def add_street(self, name: str, office: Office):
        new_id = self.street_last_id + 1
        try:
            street = Street(new_id, name, office)
            self.streets.append(street)
            self.street_last_id = new_id
            self._make_change()
            return {'success': True, 'instance': street}
        except AssertionError as e:
            return {'success': False, 'message': e}

    def add_parcel(self, office: Office, street: Street, type_: int = None):
        new_id = self.parcel_last_id + 1
        try:
            parcel = Parcel(new_id, office, street, type_)
            self.parcels.append(parcel)
            self.parcel_last_id = new_id
            self._make_change()
            return {'success': True, 'instance': parcel}
        except AssertionError as e:
            return {'success': False, 'message': e}

    def validate_login(self, username, password):
        for user in self._users:
            if user.username == username and user.password == password:
                self.authenticated_user = user
                return True
        return False

    def save(self):
        """
        Returns is_error, message
        """
        if not self.is_changed:
            response = {'success': True, 'message': 'Данные не изменены, сохранять не требуется.'}
            return response

        offices = [(office.id, office.number) for office in self.offices]
        streets = [(street.id, street.name, street.office.id) for street in self.streets]
        parcels = [(parcel.id, parcel.office.id, parcel.street.id, parcel.type) for parcel in self.parcels]
        users = [(user.id, user.username, user.password, user.permissions) for user in self._users]

        self.db.clear_data()
        self.db.insert_data(offices, streets, parcels, users)
        self.is_changed = False

        response = {'success': True, 'message': 'База данных сохранена в файл: {}'.format(self.db_name)}
        return response
