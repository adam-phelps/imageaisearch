# Generated by Django 3.1.5 on 2021-04-28 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imageais', '0015_auto_20210428_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
    ]
