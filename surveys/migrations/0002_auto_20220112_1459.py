# Generated by Django 2.2.10 on 2022-01-12 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
