# Generated by Django 2.2.14 on 2020-07-28 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20200728_1339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='date',
            new_name='purchase_date',
        ),
        migrations.AddField(
            model_name='purchase',
            name='expiration_date',
            field=models.DateField(auto_now=True),
        ),
    ]
