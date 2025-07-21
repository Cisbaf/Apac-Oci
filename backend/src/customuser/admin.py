from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('full', 'cpf', 'email', 'role', 'city', 'is_staff')
    list_filter = ('role', 'city', 'is_staff', 'is_superuser')
    
    fieldsets = (
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Configurações Específicas', {'fields': ('role', 'city')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Modificar Usuário', {'fields': ('username', 'password')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'username', 
                'email', 
                'password1', 
                'password2', 
                'role',
                'city',
                'is_staff'
            ),
        }),
    )
    
    search_fields = ('username', 'email', 'city__name')
    ordering = ('username',)

    @admin.display(description="Nome Completo")
    def full(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    @admin.display(description="CPF")
    def cpf(self, obj):
        return obj.username
