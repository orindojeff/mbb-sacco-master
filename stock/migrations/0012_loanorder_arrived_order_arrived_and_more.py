# Generated by Django 4.1.5 on 2023-03-23 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0011_loanorder_assigned_alter_loanorder_transaction_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanorder',
            name='arrived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='arrived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='loanorder',
            name='transaction_id',
            field=models.CharField(default='9ArLMOAwE', max_length=250),
        ),
        migrations.AlterField(
            model_name='loanorderinstallments',
            name='transaction_id',
            field=models.CharField(default='o3bynzB4h', max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default='nZFUPEnFp', max_length=250),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='transaction_id',
            field=models.CharField(default='o3bynzB4h', max_length=250),
        ),
    ]
