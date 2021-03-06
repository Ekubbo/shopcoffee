# Generated by Django 2.1.5 on 2019-03-08 08:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone_client', models.CharField(max_length=150)),
                ('adress_client', models.CharField(max_length=250)),
                ('comment', models.TextField(blank=True, max_length=700)),
                ('status', models.CharField(choices=[('Rec.', 'Received'), ('Proc.', 'Processed'), ('Tran.', 'Transmitted')], default='Rec.', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('description', models.TextField(blank=True, max_length=500)),
                ('price', models.IntegerField()),
                ('photo', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'product')},
        ),
    ]
