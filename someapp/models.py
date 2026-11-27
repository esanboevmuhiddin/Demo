from django.db import models
from django.contrib.auth.models import User


class Transport(models.TextChoices):
    KATER = 'kater', 'Катер'
    LINER = 'liner', 'Круизный лайнер'
    YAHTA = 'yahta', 'Яхта'


class Payment(models.TextChoices):
    CARD = 'card', 'Банковская карта'
    CASH = 'cash', 'Наличные'
    ONLINE = 'online', 'Онлайн-перевод'


class Status(models.TextChoices):
    NEW = 'new', 'Новая'
    IN_PROGRESS = 'progress', 'Идет обучение'
    DONE = 'done', 'Обучение завершено'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=150)
    birth_date = models.DateField('Дата рождения')
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('E-mail')

    def __str__(self):
        return self.full_name


class Application(models.Model):
    # Выборы транспорта (пример)
    TRANSPORT_CHOICES = [
        ('kater', 'Катер'),
        ('layner', 'Лайнер'),
        ('yahta', 'Яхта'),
        ('reka', 'Река'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принята'),
        ('done', 'Выполнена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    transport = models.CharField("Транспорт", max_length=20, choices=TRANSPORT_CHOICES)
    start_date = models.DateField("Дата старта")
    payment = models.CharField("Оплата", max_length=50, blank=True, null=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Заявка #{self.pk} - {self.get_transport_display()}"


class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review')
    text = models.TextField('Отзыв')
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    created_at = models.DateTimeField(auto_now_add=True)