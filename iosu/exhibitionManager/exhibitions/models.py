from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Exhibition(models.Model):
    name = models.CharField(max_length=512, verbose_name='Наименование')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    address = models.CharField(max_length=512, verbose_name='Адрес')

    def __str__(self):
        return self.name

    def clean(self):
        if self.end_date and timezone.now() >= self.end_date:
            raise ValidationError('Нельзя добавлять уже завершенные выставки')

    class Meta:
        verbose_name = 'Выставка'
        verbose_name_plural = 'Выставки'


class ExhibitionPlace(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер')
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, verbose_name='Выставка')

    def __str__(self):
        return 'Место №{}, {}'.format(self.number, self.exhibition)

    class Meta:
        unique_together = ('number', 'exhibition')
        verbose_name = 'Выставочное место'
        verbose_name_plural = 'Выставочные места'


class Company(models.Model):
    name = models.CharField(max_length=512, unique=True, verbose_name='Наименование')
    address = models.CharField(max_length=512, verbose_name='Адрес')
    email = models.EmailField(unique=True, verbose_name='Email')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'


class ParticipationExhibition(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, verbose_name='Выставка')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Предприятие')

    def __str__(self):
        return '{} в {}'.format(self.company, self.exhibition)

    class Meta:
        ordering = ('-pk',)
        unique_together = ('exhibition', 'company')
        verbose_name = 'Участие в выставке'
        verbose_name_plural = 'Участия в выставках'


class RentExhibitionPlace(models.Model):
    participation = models.ForeignKey(ParticipationExhibition, on_delete=models.CASCADE, verbose_name='Участие в выставке')
    place = models.ForeignKey(ExhibitionPlace, on_delete=models.CASCADE, verbose_name='Выставочное место')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')

    def __str__(self):
        return 'Место №{}, {}'.format(self.place.number, self.participation)

    def clean(self):
        if not (self.start_date and self.end_date and self.participation and self.place):
            return super().clean()
        if self.start_date >= self.end_date:
            raise ValidationError('Неверные даты начала и конца аренды')
        if self.start_date < self.participation.exhibition.start_date or self.end_date > self.participation.exhibition.end_date:
            raise ValidationError('Арендовать место можно только на время проведения выставки')
        if not self.participation.exhibition == self.place.exhibition:
            raise ValidationError('Выбрано место из другой выставки')
        is_busy_query = RentExhibitionPlace.objects.filter(place=self.place).exclude(start_date__gt=self.end_date).exclude(end_date__lt=self.start_date)
        if self.pk:
            is_busy_query = is_busy_query.exclude(pk=self.pk)
        if is_busy_query.exists():
            raise ValidationError('Это место в это время уже занято')
        return super().clean()

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Аренда места'
        verbose_name_plural = 'Аренда мест'


class Products(models.Model):
    name = models.CharField(max_length=512, verbose_name='Наименование')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена, руб')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Предприятие')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'company')
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'


class AdvertisementType(models.Model):
    name = models.CharField(max_length=512, unique=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип рекламы'
        verbose_name_plural = 'Типы рекламы'


class Advertisement(models.Model):
    participation = models.ForeignKey(ParticipationExhibition, on_delete=models.CASCADE, verbose_name='Участие в выставке')
    type = models.ForeignKey(AdvertisementType, on_delete=models.PROTECT, verbose_name='Тип')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена, руб')

    def __str__(self):
        return 'Реклама {} - {}'.format(self.type.name.lower(), self.participation)

    def clean(self):
        if not (self.start_date and self.end_date):
            return super().clean()
        if self.start_date >= self.end_date:
            raise ValidationError('Неверные даты начала и конца рекламы')
        return super().clean()

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'


class Ticket(models.Model):
    series = models.CharField(max_length=64, unique=True, verbose_name='Серия и номер')
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, verbose_name='Выставка')

    def __str__(self):
        return '{} на {}'.format(self.series, self.exhibition)

    def clean(self):
        if timezone.now() > self.exhibition.end_date:
            raise ValidationError('Билет приобрести нельзя, так как выставка уже закончилась')

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


class Visitor(models.Model):
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    middle_name = models.CharField(max_length=64, verbose_name='Отчество')
    phone = models.CharField(max_length=32, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')
    tickets = models.ManyToManyField(Ticket, related_name='visitors', through='VisitorsTickets')

    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)

    class Meta:
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'


class VisitorsTickets(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, verbose_name='Посетитель')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Билет')
    purchase_date = models.DateTimeField(default=timezone.now, verbose_name='Дата покупки')

    def __str__(self):
        return '{}, {}'.format(self.ticket, self.visitor)

    class Meta:
        unique_together = ('visitor', 'ticket')
        verbose_name = 'Посетитель - билет'
        verbose_name_plural = 'Посетители - билеты'
