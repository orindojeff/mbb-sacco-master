# Generated by Django 4.1.5 on 2023-01-30 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_loanorder_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanorder',
            name='transaction_id',
            field=models.CharField(default='N8dMyBUs1', max_length=250),
        ),
        migrations.AlterField(
            model_name='loanorderinstallments',
            name='transaction_id',
            field=models.CharField(default='nfQE2rAKO', max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default='6TDBxG5fg', max_length=250),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='transaction_id',
            field=models.CharField(default='nfQE2rAKO', max_length=250),
        ),
    ]
