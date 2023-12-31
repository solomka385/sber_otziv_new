# Generated by Django 4.1.5 on 2023-06-08 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anketa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50, unique=True)),
                ('number1', models.CharField(blank=True, default='Чистота салона', max_length=50, verbose_name='Критерий 1')),
                ('number2', models.CharField(blank=True, default='Пунктуальность водителя', max_length=50, verbose_name='Критерий 2')),
                ('number3', models.CharField(blank=True, default='Вежливость персонала', max_length=50, verbose_name='Критерий 3')),
                ('number4', models.CharField(blank=True, default='Заполненность транспортного средства', max_length=50, verbose_name='Критерий 4')),
                ('number5', models.CharField(blank=True, default='Температура в салоне', max_length=50, verbose_name='Критерий 5')),
                ('dop1', models.CharField(blank=True, default='', max_length=50, verbose_name='Описание критерия 1')),
                ('dop2', models.CharField(blank=True, default='', max_length=50, verbose_name='Описание критерия 2')),
                ('dop3', models.CharField(blank=True, default='', max_length=50, verbose_name='Описание критерия 3')),
                ('dop4', models.CharField(blank=True, default='', max_length=50, verbose_name='Описание критерия 4')),
                ('dop5', models.CharField(blank=True, default='', max_length=50, verbose_name='Описание критерия 5')),
            ],
        ),
        migrations.CreateModel(
            name='Opros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('time', models.TimeField(verbose_name='Дата поездки')),
                ('text', models.CharField(max_length=255, verbose_name='Отзыв')),
                ('number1', models.CharField(max_length=1)),
                ('number2', models.CharField(max_length=1)),
                ('number3', models.CharField(max_length=1)),
                ('number4', models.CharField(max_length=1)),
                ('number5', models.CharField(max_length=1)),
                ('number', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('job', models.CharField(max_length=50, verbose_name='Должность')),
                ('date_of_dirth', models.DateField(verbose_name='Дата рождения')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('number', models.CharField(max_length=12, verbose_name='Госномер')),
                ('image', models.ImageField(upload_to='qr_codes/')),
            ],
        ),
    ]
