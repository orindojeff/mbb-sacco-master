# Generated by Django 4.1.5 on 2023-03-31 08:23

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_archived_user_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialogsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dialog',
                'verbose_name_plural': 'Dialogs',
                'unique_together': {('customer', 'staff')},
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='content')),
                ('type', models.CharField(choices=[('CST_FMR', 'Finance Manager'), ('FMR_CST', 'Customer / Rider'), ('CST_SMR', 'Sales Manager'), ('SMR_CST', 'Customer / Rider')], default='CST_FMR', max_length=10, verbose_name='Feedback type')),
                ('dialog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='accounts.dialogsmodel')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
    ]
