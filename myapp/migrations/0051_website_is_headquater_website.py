# Generated by Django 2.2.6 on 2020-01-22 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0050_auto_20200120_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='is_headquater_website',
            field=models.BooleanField(default=False),
        ),
    ]
