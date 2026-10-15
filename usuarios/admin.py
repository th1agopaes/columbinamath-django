from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # admin pronto de usuários
from .models import Usuario  # models da aplicação usuários


@admin.register(Usuario)  # registra o model no painel admin
class UsuarioAdmin(UserAdmin):  # herda tudo do admin padrão de usuários
    fieldsets = UserAdmin.fieldsets + (  # tela de editar
        ("ColumbinaMath", {"fields": ("tipo",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # tela de criar
        (
            "ColumbinaMath",
            {"fields": ("email", "tipo")},
        )
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
