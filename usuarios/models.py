from django.conf import settings  # acesso ao AUTH_USER_MODEL
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
)  # usuário completo do Django, feito para ser herdado
from django.core.exceptions import (
    ValidationError,
)  # erro de validação oficial do Django
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


class PerfilAluno(models.Model):  # ficha complementar só de alunos
    class Serie(models.IntegerChoices):  # choices numéricas (série é número)
        PRIMEIRO = 1, "1º ano"  # (valor no banco, texto na tela)
        SEGUNDO = 2, "2º ano"
        TERCEIRO = 3, "3º ano"

    usuario = models.OneToOneField(  # relação 1:1 (um usuário, no máximo um perfil)
        settings.AUTH_USER_MODEL,  # aponta para o usuário oficial, sem importar a classe
        on_delete=models.CASCADE,  # apagou o usuário, apaga o perfil junto
        related_name="perfil_aluno",  # caminho de volta: usuario.perfil_aluno
        limit_choices_to={"tipo": Usuario.Tipo.ALUNO},  # formulários só listam alunos
        verbose_name="usuário",  # nome amigável no admin
    )
    serie = models.PositiveSmallIntegerField(  # inteiro pequeno, sem negativos
        "série",  # nome amigável
        choices=Serie.choices,  # só aceita 1, 2 ou 3
    )

    class Meta:
        verbose_name = "perfil de aluno"
        verbose_name_plural = "perfis de alunos"

    def __str__(self):
        return (
            f"{self.usuario} - {self.get_serie_display()}"  # ex: "Ana Souza - 2º ano"
        )

    def clean(self):  # validação de regra de negócio
        super().clean()  # mantém as validações do pai
        if (
            self.usuario_id and self.usuario.tipo != Usuario.Tipo.ALUNO
        ):  # usuario_id: só o id, sem consulta extra
            raise ValidationError(
                "Somente usuários do tipo aluno podem ter perfil de aluno."
            )
