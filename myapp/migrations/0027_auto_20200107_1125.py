# Generated by Django 2.2.6 on 2020-01-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_auto_20200107_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='website_company_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
