# Generated by Django 2.2 on 2021-05-23 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_messenge_nameuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='messenge',
            name='imgUrl',
            field=models.CharField(max_length=1000000, null=True),
        ),
    ]
