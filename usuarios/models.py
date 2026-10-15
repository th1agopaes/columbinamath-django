from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
)  # usuário completo do Django, feito para ser herdado
from django.db import models  # tipos de campo (CharField, EmailField...)


class UsuarioManager(UserManager):  # herda a recepção padrão de usuários
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # **extra_fields = dicionário com os demais campos enviados
        extra_fields.setdefault(
            "tipo", self.model.Tipo.ADMIN
        )  # se não informado o tipo, vira ADMIN
        return super().create_superuser(
            username, email, password, **extra_fields
        )  # o pai faz o resto


class Usuario(AbstractUser):  # herança: ganha tudo do AbstractUser
    class Tipo(models.TextChoices):  # o enum TipoUsuario do diagrama de classes
        ALUNO = "ALUNO", "Aluno"  # (valor salvo no banco, texto exibido na tela)
        PROFESSOR = "PROFESSOR", "Professor"
        ADMIN = "ADMIN", "Administrador"

    email = models.EmailField(
        "e-mail", unique=True
    )  # sobrescreve o e-mail herdado, agora é único
    tipo = models.CharField(
        "tipo",  # nome do campo
        max_length=20,  # tamanho máximo
        choices=Tipo.choices,  # só aceita os 3 valores acima
        default=Tipo.ALUNO,  # o usuário comum é aluno
    )

    objects = UsuarioManager()  # troca a recepção padrão de usuários pela minha

    class Meta:  # as configurações do model
        verbose_name = "usuário"  # nome no singular, no admin
        verbose_name_plural = "usuários"  # nome no plural

    def __str__(self):  # como o objeto aparece como texto
        return self.get_full_name() or self.username  # nome completo, se vazio o login
