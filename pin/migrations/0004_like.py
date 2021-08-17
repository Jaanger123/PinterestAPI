# Generated by Django 3.2.6 on 2021-08-17 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pin', '0003_auto_20210816_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='pin.pin')),
            ],
        ),
    ]