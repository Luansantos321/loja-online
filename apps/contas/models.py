from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone"
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=True,
        blank=True,
        verbose_name="CPF"
    )

    foto = models.ImageField(
        upload_to="usuarios/",
        default="usuarios/default.png",
        blank=True,
        verbose_name="Foto"
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["first_name"]

    def __str__(self):
        return self.get_full_name() or self.username