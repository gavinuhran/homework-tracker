# Generated by Django 3.2.8 on 2021-11-21 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]