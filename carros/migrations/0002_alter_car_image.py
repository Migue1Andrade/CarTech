# Generated by Django 4.2 on 2023-04-13 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='car_images'),
        ),
    ]
