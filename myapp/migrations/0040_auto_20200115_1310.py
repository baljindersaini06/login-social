# Generated by Django 2.2.6 on 2020-01-15 13:10

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_merge_20200114_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='countries',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
