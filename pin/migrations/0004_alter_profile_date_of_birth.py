# Generated by Django 3.2.6 on 2021-08-20 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0003_auto_20210820_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
