# Generated by Django 3.2.8 on 2021-11-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0012_alter_user_saldo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='saldo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, max_length=20),
        ),
    ]
