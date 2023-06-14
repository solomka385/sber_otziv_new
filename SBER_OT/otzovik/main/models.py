from django.db import models



class Personal(models.Model):
    user = models.CharField(max_length=50)
    name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    job = models.CharField(max_length=50,verbose_name='Должность')
    date_of_dirth = models.DateField(verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField()

    def get_absolute_url(self):
        return '/personal'


class Transport(models.Model):
    user = models.CharField(max_length=50)
    model = models.CharField(max_length=50, verbose_name='Модель')
    number = models.CharField(max_length=12,verbose_name='Госномер')
    image = models.ImageField(upload_to='qr_codes/')
    def get_absolute_url(self):
        return '/transport'

class Anketa(models.Model):
    user = models.CharField(max_length=50, unique=True)
    number1 = models.CharField(max_length=50, blank=True, verbose_name= 'Критерий 1', default='Чистота салона')
    number2 = models.CharField(max_length=50,blank=True, verbose_name= 'Критерий 2', default= 'Пунктуальность водителя')
    number3 = models.CharField(max_length=50,blank=True, verbose_name= 'Критерий 3', default='Вежливость персонала')
    number4 = models.CharField(max_length=50,blank=True, verbose_name= 'Критерий 4', default='Заполненность транспортного средства')
    number5 = models.CharField(max_length=50,blank=True, verbose_name= 'Критерий 5', default='Температура в салоне')
    dop1 = models.CharField(max_length=50, blank=True, verbose_name='Описание критерия 1', default='')
    dop2 = models.CharField(max_length=50, blank=True, verbose_name='Описание критерия 2', default='')
    dop3 = models.CharField(max_length=50, blank=True, verbose_name='Описание критерия 3', default='')
    dop4 = models.CharField(max_length=50, blank=True, verbose_name='Описание критерия 4', default='')
    dop5 = models.CharField(max_length=50, blank=True, verbose_name='Описание критерия 5', default='')

    def get_absolute_url(self):
        return '/'

class Opros(models.Model):
    anketa = Anketa()
    user = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now=True, verbose_name='Дата отзыва')
    text = models.CharField(max_length=255, verbose_name='Отзыв')
    number1 = models.CharField(max_length=1 )
    number2 = models.CharField(max_length=1)
    number3 = models.CharField(max_length=1)
    number4 = models.CharField(max_length=1)
    number5 = models.CharField(max_length=10)
    number = models.CharField(max_length=12)
    def get_absolute_url(self):
        return '/opros'