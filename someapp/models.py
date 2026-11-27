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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    transport = models.CharField(max_length=20, choices=Transport.choices, verbose_name='Вид транспорта')
    start_date = models.DateField('Дата начала обучения')
    payment = models.CharField(max_length=20, choices=Payment.choices, verbose_name='Способ оплаты')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.pk} — {self.get_transport_display()}'


class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review')
    text = models.TextField('Отзыв')
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    created_at = models.DateTimeField(auto_now_add=True)