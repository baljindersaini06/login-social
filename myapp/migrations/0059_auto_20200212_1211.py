# Generated by Django 2.2.6 on 2020-02-12 12:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0058_meeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='asset_tag_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documents',
            name='content',
            field=models.TextField(),
        ),
    ]
