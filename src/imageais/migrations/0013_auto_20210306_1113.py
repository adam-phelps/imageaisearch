# Generated by Django 3.1.5 on 2021-03-06 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageais', '0012_auto_20210306_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimage',
            name='public_id',
            field=models.CharField(default='d177980110ba', max_length=20),
        ),
    ]
