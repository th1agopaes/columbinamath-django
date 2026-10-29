from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # admin pronto de usuários

from .models import PerfilAluno, Usuario  # models da aplicação usuários


class PerfilAlunoInline(
    admin.StackedInline
):  # mostra o perfil dentro da página do usuário
    model = PerfilAluno
    can_delete = False
    verbose_name_plural = "perfil de aluno"


@admin.register(Usuario)  # registra o model no painel admin
class UsuarioAdmin(UserAdmin):  # herda tudo do admin padrão de usuários
    inlines = (PerfilAlunoInline,)  # liga o inline à página do usuário

    fieldsets = UserAdmin.fieldsets + (  # tela de editar
        ("ColumbinaMath", {"fields": ("tipo",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # tela de criar
        ("ColumbinaMath", {"fields": ("email", "tipo")}),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "tipo",
        "is_active",
    )  # colunas da listagem
    list_filter = ("tipo", "is_active")  # filtros na lateral
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )  # campos de busca

    def get_inline_instances(self, request, obj=None):  # decide quando o inline aparece
        if (
            obj is None or obj.tipo != Usuario.Tipo.ALUNO
        ):  # na criação ou se não for aluno
            return []  # não mostra
        return super().get_inline_instances(request, obj)  # aluno existente: mostra
