from django.contrib.auth.models import (
    AbstractUser,
)  # usuário completo do Django, feito para ser herdado
from django.db import models  # tipos de campo (CharField, EmailField...)


class Usuario(AbstractUser):  # herança: ganha tudo do AbstractUser
    class Tipo(models.TextChoices):  # o enum TipoUsuario do diagrama de classes
        ALUNO = "ALUNO", "Aluno"  # (valor salvo no banco, texto exibido na tela)
        PROFESSOR = "PROFESSOR", "Professor"
        ADMIN = "ADMIN", "Administrador"

    email = models.EmailField("e-mail", unique=True)  # sobrescreve o e-mail herdado, agora é único
    tipo = models.CharField(
        "tipo",  # nome do campo
        max_length=20,  # tamanho máximo
        choices=Tipo.choices,  # só aceita os 3 valores acima
        default=Tipo.ALUNO, # o usuário comum é aluno
    )

    class Meta:  # as configurações do model
        verbose_name = "usuário"  # nome no singular, no admin
        verbose_name_plural = "usuários"  # nome no plural

    def __str__(self):  # como o objeto aparece como texto
        return self.get_full_name() or self.username  # nome completo, se vazio o login
