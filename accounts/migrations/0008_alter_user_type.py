# Generated by Django 4.2.3 on 2023-07-23 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('DR', 'Driver'), ('FM', 'Finance'), ('SM', 'Sales'), ('RD', 'Rider'), ('CM', 'Customer'), ('SP', 'Supplier'), ('DP', 'DP')], default='CM', max_length=2),
        ),
    ]
