# Generated by Django 2.1.5 on 2019-02-28 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20190228_0029'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'product')},
        ),
    ]
