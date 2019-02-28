# Generated by Django 2.1.5 on 2019-02-28 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20190228_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Rec.', 'Received'), ('Proc.', 'Processed'), ('Tran.', 'Transmitted')], default='Rec.', max_length=20),
        ),
    ]
