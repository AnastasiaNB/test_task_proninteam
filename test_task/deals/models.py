from django.contrib.auth.models import User
from django.db import models


class Gem(models.Model):
    """
    Gem model
    """
    gem_name = models.CharField(
        max_length=30,
        verbose_name='Название камня'
    )


class Deal(models.Model):
    """
    Deal model
    """
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
        related_name='deals'
    )
    item = models.ForeignKey(
        Gem,
        on_delete=models.CASCADE,
        verbose_name='Камень',
        related_name='deals'
    )
    total = models.IntegerField(
        verbose_name='Сумма'
    )
    quantity = models.IntegerField(
        verbose_name='Количество'
    )
    date = models.DateTimeField(
        verbose_name='Дата'
    )
