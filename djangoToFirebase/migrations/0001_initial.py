# Generated by Django 4.1.2 on 2023-01-26 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='smartBin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binName', models.CharField(max_length=20)),
                ('binDate', models.DateTimeField()),
                ('binTime', models.TimeField()),
                ('battery', models.IntegerField(verbose_name=100)),
                ('binLevel1', models.IntegerField(verbose_name=100)),
                ('binLevel2', models.IntegerField(verbose_name=100)),
            ],
        ),
    ]
