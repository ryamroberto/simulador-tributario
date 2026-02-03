from django.db import models

class TimeStampedModel(models.Model):
    """
    Modelo abstrato para adicionar campos de data de criação e atualização.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        abstract = True