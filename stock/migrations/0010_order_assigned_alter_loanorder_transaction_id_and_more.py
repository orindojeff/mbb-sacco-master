# Generated by Django 4.1.5 on 2023-03-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0009_alter_loanorder_transaction_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='assigned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='loanorder',
            name='transaction_id',
            field=models.CharField(default='Lq3GuQH1T', max_length=250),
        ),
        migrations.AlterField(
            model_name='loanorderinstallments',
            name='transaction_id',
            field=models.CharField(default='cMFKhmfpC', max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default='WPgdP9CVS', max_length=250),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='transaction_id',
            field=models.CharField(default='cMFKhmfpC', max_length=250),
        ),
    ]
