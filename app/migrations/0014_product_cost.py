# Generated by Django 2.2.14 on 2020-07-28 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20200728_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]
