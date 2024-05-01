import random
import string
from decimal import Decimal
from django.utils import timezone
from django.core.management.base import BaseCommand

from exhibitions.models import Exhibition, ExhibitionPlace, Visitor, Ticket, VisitorsTickets, Company, Products

NUM_VISITORS = 20

class Command(BaseCommand):
    help = 'Populate tables with test data'

    exhibitions = [
        {'name': 'Выставка искусства "Модерн"', 'address': 'ул. Примерная, д. 123, г. Примерный'},
        {'name': 'Выставка современной живописи', 'address': 'пр. Перспективный, д. 45, г. Перспективный'},
        {'name': 'Международная выставка дизайна', 'address': 'ул. Фантазийная, д. 67, г. Фантазия'},
        {'name': 'Выставка фотографий "Города мира"', 'address': 'пл. Красивая, д. 89, г. Красивый'},
        {'name': 'Выставка скульптуры "Гранитные формы"', 'address': 'пр. Массивный, д. 34, г. Массивный'},
        {'name': 'Выставка текстильного искусства', 'address': 'ул. Ткацкая, д. 56, г. Ткачи'},
        {'name': 'Выставка антиквариата и коллекционирования', 'address': 'пер. Старый, д. 12, г. Стародавний'},
        {'name': 'Выставка садоводства и ландшафтного дизайна', 'address': 'аллея Природная, д. 78, г. Природа'},
        {'name': 'Выставка научно-технических достижений', 'address': 'пл. Изобретательная, д. 23, г. Изобретатель'},
        {'name': 'Выставка кулинарного искусства', 'address': 'ул. Поварская, д. 10, г. Повари'},
        {'name': 'Выставка моды и стиля', 'address': 'пр. Модельный, д. 5, г. Модельный'},
        {'name': 'Выставка театрального искусства', 'address': 'пл. Драматическая, д. 32, г. Драматический'}
    ]

    companies = [
        {'name': 'АртМастер', 'address': 'ул. Художественная, д. 10, г. Искусствовед', 'email': 'artmaster@example.com', 'products': [{'name': 'Картина "Абстракция"', 'amount': 5, 'price': 25000}, {'name': 'Скульптура "Мраморная женщина"', 'amount': 2, 'price': 45000}, {'name': 'Фоторамка "Винтаж"', 'amount': 10, 'price': 1500}]},
        {'name': 'ТехноПрогресс', 'address': 'пр. Научный, д. 5, г. Технополис', 'email': 'techprogress@example.com', 'products': [{'name': 'Ноутбук "Инновация"', 'amount': 20, 'price': 60000}, {'name': '3D Принтер "Эволюция"', 'amount': 3, 'price': 120000}, {'name': 'Умные часы "Футуризм"', 'amount': 15, 'price': 5000}]},
        {'name': 'ДизайнСтудия', 'address': 'ул. Творческая, д. 15, г. Креативно', 'email': 'designstudio@example.com', 'products': [{'name': 'Дизайнерский стул "Современность"', 'amount': 8, 'price': 10000}, {'name': 'Декоративная подушка "АртДеко"', 'amount': 12, 'price': 1200}, {'name': 'Дизайнерский коврик "Эстетика"', 'amount': 6, 'price': 3000}]},
        {'name': 'ФотоКорпорация', 'address': 'пл. Фотографическая, д. 20, г. Фотосити', 'email': 'photocorp@example.com', 'products': [{'name': 'Цифровая камера "Профессионал"', 'amount': 7, 'price': 35000}, {'name': 'Фотоальбом "Любимые моменты"', 'amount': 15, 'price': 800}, {'name': 'Фоторамка "Стеклянная"', 'amount': 20, 'price': 1200}]},
        {'name': 'ИнновацииЛаб', 'address': 'пр. Изобретательный, д. 30, г. Инновацион', 'email': 'innovlab@example.com', 'products': [{'name': 'Робот-пылесос "Умничка"', 'amount': 10, 'price': 20000}, {'name': 'Умный дом "Будущее"', 'amount': 3, 'price': 150000}, {'name': 'Беспроводные наушники "Свобода"', 'amount': 25, 'price': 3000}]},
        {'name': 'АнтиквариатИзыск', 'address': 'ул. Раритетная, д. 7, г. Старинов', 'email': 'antiques@example.com', 'products': [{'name': 'Статуэтка "Историческая личность"', 'amount': 4, 'price': 25000}, {'name': 'Антикварная ваза "Раритет"', 'amount': 2, 'price': 50000}, {'name': 'Старинный часы "Уникальные"', 'amount': 6, 'price': 18000}]},
        {'name': 'СадоТворчество', 'address': 'аллея Ландшафтная, д. 12, г. Пейзажи', 'email': 'gardencraft@example.com', 'products': [{'name': 'Садовые фонари "Романтика"', 'amount': 20, 'price': 1500}, {'name': 'Цветочный горшок "Элегантность"', 'amount': 30, 'price': 800}, {'name': 'Садовый фонтан "Гармония"', 'amount': 5, 'price': 20000}]},
        {'name': 'Мода и Стиль', 'address': 'пр. Модельный, д. 3, г. Моделево', 'email': 'fashionstyle@example.com', 'products': [{'name': 'Платье "Вечерний взгляд"', 'amount': 10, 'price': 5000}, {'name': 'Мужской костюм "Элегантный"', 'amount': 15, 'price': 10000}, {'name': 'Сумка "Лаконичная"', 'amount': 25, 'price': 3000}]},
        {'name': 'Кулинарное искусство', 'address': 'ул. Кулинарная, д. 25, г. Кулинария', 'email': 'culinary@example.com', 'products': [{'name': 'Кулинарная книга "Гастрономия"', 'amount': 8, 'price': 1500}, {'name': 'Кухонный набор "Шеф-повар"', 'amount': 12, 'price': 2000}, {'name': 'Кухонные принадлежности "Удобство"', 'amount': 20, 'price': 1000}]},
        {'name': 'Театральные костюмы', 'address': 'пл. Драматическая, д. 8, г. Театров', 'email': 'theatercostumes@example.com', 'products': [{'name': 'Костюм "Исторический"', 'amount': 6, 'price': 8000}, {'name': 'Платье "Фантазия"', 'amount': 10, 'price': 6000}, {'name': 'Маска "Таинственность"', 'amount': 15, 'price': 500}]},
        {'name': 'Мебельный Мир', 'address': 'ул. Мебельная, д. 17, г. Мебельград', 'email': 'furnitureworld@example.com', 'products': [{'name': 'Диван "Комфорт"', 'amount': 3, 'price': 35000}, {'name': 'Стол "Элегант"', 'amount': 7, 'price': 12000}, {'name': 'Шкаф "Простор"', 'amount': 12, 'price': 18000}]},
        {'name': 'СтройТехника', 'address': 'пр. Строительный, д. 40, г. Строитель', 'email': 'construction@example.com', 'products': []},
        {'name': 'Авто Мастер', 'address': 'ул. Автомобильная, д. 22, г. Автомеханика', 'email': 'autocare@example.com', 'products': []},
        {'name': 'Туристические Путевки', 'address': 'пл. Туристическая, д. 14, г. Туристово', 'email': 'travelcompany@example.com', 'products': []},
        {'name': 'Ювелирные изделия', 'address': 'ул. Ювелирная, д. 9, г. Ювелирный', 'email': 'jewelry@example.com', 'products': []},
    ]

    last_names = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов',
                  'Новиков', 'Федоров', 'Морозов', 'Волков', 'Алексеев', 'Лебедев', 'Семенов', 'Егоров',
                  'Павлов', 'Козлов', 'Степанов', 'Николаев']
    first_names_male = ['Иван', 'Дмитрий', 'Александр', 'Андрей', 'Артем', 'Михаил', 'Сергей', 'Николай',
                        'Максим', 'Павел', 'Денис', 'Егор', 'Илья', 'Кирилл', 'Тимофей', 'Антон',
                        'Владимир', 'Глеб', 'Роман', 'Ярослав']
    first_names_female = ['Анна', 'Елена', 'Мария', 'Ольга', 'Татьяна', 'Наталья', 'Ирина', 'Екатерина',
                          'Светлана', 'Александра', 'Виктория', 'Ксения', 'Анастасия', 'Евгения', 'Дарья',
                          'Евдокия', 'Любовь', 'София', 'Алиса', 'Валентина']
    middle_names = ['Иванович', 'Дмитриевич', 'Александрович', 'Андреевич', 'Артемович', 'Михайлович',
                    'Сергеевич', 'Николаевич', 'Максимович', 'Павлович', 'Денисович', 'Егорович', 'Маркович',
                    'Кириллович', 'Тимофеевич', 'Антонович', 'Владимирович', 'Глебович', 'Романович',
                    'Ярославович']
    phones = ['+7 (123) 456-78-90', '+7 (234) 567-89-01', '+7 (345) 678-90-12', '+7 (456) 789-01-23',
              '+7 (567) 890-12-34', '+7 (678) 901-23-45', '+7 (789) 012-34-56', '+7 (890) 123-45-67',
              '+7 (901) 234-56-78', '+7 (012) 345-67-89']
    emails = ['example1@domain.ru', 'example2@domain.ru', 'example3@domain.ru', 'example4@domain.ru',
              'example5@domain.ru', 'example6@domain.ru', 'example7@domain.ru', 'example8@domain.ru',
              'example9@domain.ru', 'example10@domain.ru']

    @staticmethod
    def get_random_datetime():
        return timezone.now() - timezone.timedelta(
            days=random.randint(1, 365),
            hours=random.randint(1, 24),
            minutes=random.randint(1, 60),
        )

    @staticmethod
    def get_random_future_datetime():
        return timezone.now() + timezone.timedelta(
            days=random.randint(1, 365),
            hours=random.randint(1, 24),
            minutes=random.randint(1, 60),
        )

    def handle(self, *args, **kwargs):

        for exhibition in self.exhibitions:

            # Exhibitions

            exhibition_new = Exhibition.objects.create(
                name=exhibition['name'],
                start_date=self.get_random_datetime(),
                end_date=self.get_random_future_datetime(),
                address=exhibition['address'],
            )

            # ExhibitionPlaces

            for _ in range(6):
                try:
                    ExhibitionPlace.objects.create(
                        number=random.randint(0, 100),
                        exhibition=exhibition_new,
                    )
                except Exception:
                    pass

        for company in self.companies:

            # Companies

            company_obj = Company.objects.create(
                name=company['name'],
                address=company['address'],
                email=company['email'],
            )

            # Products

            for product in company['products']:
                Products.objects.create(
                    name=product['name'],
                    amount=product['amount'],
                    price=Decimal.from_float(float(product['price'])),
                    company=company_obj,
                )

        for _ in range(NUM_VISITORS):

            # Visitors

            last_name = random.choice(self.last_names)
            middle_name = random.choice(self.middle_names)
            if random.choice([True, False]):  # is female
                first_name = random.choice(self.first_names_female)
                last_name += 'а'
                middle_name = middle_name[:-2] + 'на'
            else:
                first_name = random.choice(self.first_names_male)
            phone = random.choice(self.phones)
            email = random.choice(self.emails)

            visitor = Visitor.objects.create(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                phone=phone,
                email=email
            )

            # Tickets

            ticket = Ticket.objects.create(
                series=''.join(random.choices(string.ascii_uppercase, k=2)) +
                       ''.join(random.choices(string.digits, k=6)),
                exhibition=Exhibition.objects.get(pk=random.randint(1, len(self.exhibitions))),
            )

            # Visitors - tickets

            VisitorsTickets.objects.create(
                visitor=visitor,
                ticket=ticket,
                purchase_date=self.get_random_datetime(),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created'))
