# Generated by Django 2.2.6 on 2020-01-17 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0046_auto_20200117_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Package_selected', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Package')),
                ('companys_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='myapp.Company')),
            ],
        ),
    ]
