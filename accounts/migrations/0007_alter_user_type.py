# Generated by Django 4.1.7 on 2023-04-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('DR', 'Driver'), ('FM', 'Finance'), ('SM', 'Sales'), ('RD', 'Rider'), ('CM', 'Customer'), ('SP', 'Supplier')], default='CM', max_length=2),
        ),
    ]
