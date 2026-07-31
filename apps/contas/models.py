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


from django.db import models
from django.conf import settings


class Endereco(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='endereco'
    )
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.cidade}/{self.estado}'