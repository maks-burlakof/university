from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class JobPosition(models.Model):
    name = models.CharField(max_length=128, default=None, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Учетная запись')
    first_name = models.CharField(max_length=64, default=None, verbose_name='Имя')
    middle_name = models.CharField(max_length=64, default=None, verbose_name='Отчество')
    last_name = models.CharField(max_length=64, default=None, verbose_name='Фамилия')
    gender = models.CharField(max_length=1, choices=[('m', 'Мужской'), ('f', 'Женский')], verbose_name='Пол')
    position = models.ForeignKey(JobPosition, on_delete=models.PROTECT, default=None, verbose_name='Должность')

    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)

    class Meta:
        verbose_name = 'Рабочий'
        verbose_name_plural = 'Рабочие'


class Product(models.Model):
    name = models.CharField(max_length=128, default=None, verbose_name='Название')
    average_production_time = models.PositiveIntegerField(default=None, verbose_name='Среднее время изготовления (мин)', validators=[MinValueValidator(1),])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class EquipmentType(models.Model):
    name = models.CharField(max_length=128, default=None, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'


class Equipment(models.Model):
    name = models.CharField(max_length=128, default=None, verbose_name='Наименование')
    type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT, default=None, verbose_name='Тип')
    date_of_commissioning = models.DateTimeField(default=timezone.now, verbose_name='Дата ввода в эксплуатацию')
    date_of_last_service = models.DateTimeField(default=timezone.now, verbose_name='Дата последнего обслуживания')
    responsible_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                             verbose_name='Ответственный сотрудник')

    def clean(self):
        if self.date_of_last_service < self.date_of_commissioning:
            raise ValidationError('Последнее обслуживание оборудования не может быть раньше, чем дата ввода его в эксплуатацию.')
        if self.date_of_commissioning > timezone.now() or self.date_of_last_service > timezone.now():
            raise ValidationError('Даты не могут быть позже, чем текущая дата.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обслуживаемое оборудование'
        verbose_name_plural = 'Обслуживаемое оборудование'


class Tools(models.Model):
    name = models.CharField(max_length=128, default=None, verbose_name='Наименование')
    total_amount = models.PositiveIntegerField(default=None, verbose_name='Общее количество')
    wear_degree = models.PositiveSmallIntegerField(default=1000, validators=[MaxValueValidator(1000)],
                                                   verbose_name='Степень износа',
                                                   help_text='Значение равное нулю означает, что инструменты нуждаются в ремонте')

    def save(self, *args, **kwargs):
        if self.wear_degree < 0:
            self.wear_degree = 0
        super(Tools, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'


class TechnologicalMap(models.Model):
    number = models.CharField(max_length=32, default=None, verbose_name='Номер')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=None, verbose_name='Изделие')
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, default=None, verbose_name='Оборудование')
    tools = models.ManyToManyField(Tools, through='TechnologicalMapsTools')

    def __str__(self):
        return '№{}'.format(self.number)

    class Meta:
        verbose_name = 'Технологическая карта'
        verbose_name_plural = 'Технологические карты'


class TechnologicalMapsTools(models.Model):
    technological_map = models.ForeignKey(TechnologicalMap, on_delete=models.CASCADE, default=None, verbose_name='Технологическая карта')
    tools = models.ForeignKey(Tools, on_delete=models.CASCADE, default=None, verbose_name='Инструмент')
    number_of_required_tools = models.PositiveIntegerField(default=None, verbose_name='Количество требуемых инструментов', validators=[MinValueValidator(1),])

    def __str__(self):
        return '{} - {} шт. {}'.format(self.technological_map, self.number_of_required_tools, self.tools)

    class Meta:
        verbose_name = 'Технологическая карта - Инструменты'
        verbose_name_plural = 'Технологические карты - Инструменты'


class Production(models.Model):
    technological_map = models.ForeignKey(TechnologicalMap, on_delete=models.PROTECT, default=None, verbose_name='Технологическая карта')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Дата начала изготовления')
    end_date = models.DateTimeField(default=None, null=True, blank=True, verbose_name='Дата окончания изготовления')
    number_of_required_products = models.PositiveIntegerField(default=None, verbose_name='Количество требуемых изделий', validators=[MinValueValidator(1),])
    number_of_defects = models.PositiveIntegerField(default=None, null=True, blank=True, verbose_name='Количество брака')
    is_finished = models.BooleanField(default=False, verbose_name='Завершено')

    def time_efficiency(self):
        if self.end_date:
            average_time = self.number_of_required_products * self.technological_map.product.average_production_time
            td = self.end_date - self.start_date
            completion_time = td.days * 1440 + td.seconds // 60
            return '{}%'.format(average_time * 100 // completion_time)
        return None

    def amount_efficiency(self):
        if self.end_date and self.number_of_defects is not None:
            return '{}%'.format(100 - (self.number_of_defects * 100 // self.number_of_required_products))
        return None

    time_efficiency.short_description = 'Коэф. времени'
    amount_efficiency.short_description = 'Коэф. количества'

    def __init__(self, *args, **kwargs):
        super(Production, self).__init__(*args, **kwargs)
        self._old_end_date = self.end_date
        self._old_number_of_required_products = self.number_of_required_products

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError('Дата конца производства должна быть позже, чем дата его начала.')
        if self.start_date > timezone.now() or (self.end_date and self.end_date > timezone.now()):
            raise ValidationError('Даты не могут быть позже, чем текущая дата.')
        if self._old_number_of_required_products and self._old_number_of_required_products != self.number_of_required_products:
            raise ValidationError('Нельзя изменять количество требуемых изделий.')
        if not self.pk and self.technological_map:
            maps_tools = TechnologicalMapsTools.objects.select_related('tools').filter(technological_map=self.technological_map)
            for map_tool in maps_tools:
                tool = map_tool.tools
                needed_amount = map_tool.number_of_required_tools * self.number_of_required_products
                if tool.total_amount < needed_amount:
                    raise ValidationError('Не хватает инструментов "{}". Имеется {} шт, требуется {} шт.'.format(
                        tool.name, tool.total_amount, needed_amount
                    ))

    def save(self, *args, **kwargs):
        def start_production():
            maps_tools = TechnologicalMapsTools.objects.select_related('tools').filter(technological_map=self.technological_map)
            for map_tool in maps_tools:
                tool = map_tool.tools
                tool.total_amount -= map_tool.number_of_required_tools * self.number_of_required_products
                tool.save(update_fields=['total_amount'])

        def finish_production():
            maps_tools = TechnologicalMapsTools.objects.select_related('tools').filter(technological_map=self.technological_map)
            for map_tool in maps_tools:
                tool = map_tool.tools
                tool.total_amount += map_tool.number_of_required_tools * self.number_of_required_products
                tool.wear_degree -= (1 * map_tool.number_of_required_tools) * self.number_of_required_products
                tool.save(update_fields=['wear_degree', 'total_amount'])
            self.is_finished = True

        if not self.pk:
            start_production()
        if not self.pk and self.end_date and not self.is_finished:
            finish_production()
        elif self.pk and self.end_date and not self._old_end_date and not self.is_finished:
            finish_production()
        super(Production, self).save(*args, **kwargs)

    def __str__(self):
        return '№{} по карте {}'.format(self.id, self.technological_map)

    class Meta:
        verbose_name = 'Изготовление'
        verbose_name_plural = 'Изготовление'
