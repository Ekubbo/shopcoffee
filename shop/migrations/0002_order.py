# Generated by Django 2.1.5 on 2019-02-05 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя клиента')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия клиента')),
                ('phone_client', models.CharField(max_length=150, verbose_name='Телефон клиента')),
                ('adress_client', models.CharField(max_length=250, verbose_name='Адрес клиента')),
                ('status', models.CharField(choices=[('Пол.', 'Получено'), ('Обр.', 'Обработано'), ('Отп.', 'Отправлено')], default='Пол.', max_length=20, verbose_name='Статус')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-date_created'],
            },
        ),
    ]