# Generated by Django 2.2.15 on 2020-08-04 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20200804_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='vendor',
            field=models.CharField(choices=[('oficina', 'Oficina'), ('lady', 'Lady'), ('sugey', 'Sugey'), ('aracelli', 'Aracelli'), ('jasmina', 'Jasmina')], default='oficina', max_length=10),
        ),
    ]