# Generated by Django 4.1.7 on 2023-04-03 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0011_alter_loanaccount_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
