# Generated by Django 4.1.5 on 2023-01-31 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_alter_loanorder_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanorder',
            name='transaction_id',
            field=models.CharField(default='SauGcAcoU', max_length=250),
        ),
        migrations.AlterField(
            model_name='loanorderinstallments',
            name='transaction_id',
            field=models.CharField(default='mLL4s2aEv', max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default='n4FgOHWUJ', max_length=250),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='transaction_id',
            field=models.CharField(default='mLL4s2aEv', max_length=250),
        ),
    ]
