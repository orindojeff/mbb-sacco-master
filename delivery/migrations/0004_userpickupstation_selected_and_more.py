# Generated by Django 4.1.5 on 2023-03-22 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_alter_loanorderdelivery_station_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpickupstation',
            name='selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='loanorderdelivery',
            name='status',
            field=models.CharField(choices=[('PG', 'Pending'), ('IT', 'In Transit'), ('AR', 'Arrived')], default='PG', max_length=2),
        ),
        migrations.AlterField(
            model_name='orderdelivery',
            name='status',
            field=models.CharField(choices=[('PG', 'Pending'), ('IT', 'In Transit'), ('AR', 'Arrived')], default='PG', max_length=2),
        ),
    ]
