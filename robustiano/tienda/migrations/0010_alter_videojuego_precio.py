# Generated by Django 3.2.8 on 2021-11-23 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0009_alter_videojuego_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videojuego',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, max_length=20),
        ),
    ]