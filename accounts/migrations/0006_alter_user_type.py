# Generated by Django 4.1.7 on 2023-04-03 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_dialogsmodel_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('DR', 'Driver'), ('FM', 'Finance'), ('SM', 'Sales'), ('RD', 'Rider'), ('CM', 'Customer'), ('SP', 'SUPPLIER')], default='CM', max_length=2),
        ),
    ]