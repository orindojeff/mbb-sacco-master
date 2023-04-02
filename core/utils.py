from random import randint

from django.db import models


def generate_key(minlength=20, maxlength=20, use_lower=True, use_upper=True, use_numbers=True, use_special=False):
    charset = ''
    if use_lower:
        charset += "abcdefghijklmnopqrstuvwxyz"
    if use_upper:
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers:
        charset += "123456789"
    if use_special:
        charset += "~@#$%^*()_+-={}|]["
    if minlength > maxlength:
        length = randint(maxlength, minlength)
    else:
        length = randint(minlength, maxlength)
    key = ''
    for i in range(0, length):
        key += charset[(randint(0, len(charset) - 1))]
    return key


class TimeStampModel(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']
