# Generated by Django 3.2 on 2021-05-01 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('RE', 'RECEIVED'), ('DI', 'DISPATCHED'), ('DE', 'DELIVERED')], default='RE', max_length=2),
        ),
    ]
