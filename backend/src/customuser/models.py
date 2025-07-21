from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from city.models import CityModel
from apac_core.domain.entities.user import User
from apac_core.domain.entities.user_role import UserRole as UserRoleEntity


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('role', UserRole.GUEST)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(username, email, password, **extra_fields)


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Administrador'
    REQUESTER = 'requester', 'Solicitante'
    AUTHORIZER = 'authorizer', 'Autorizador'
    GUEST = 'guest', 'Visitante'


class CustomUser(AbstractUser):
    city = models.ForeignKey(verbose_name="Cidade", to=CityModel, on_delete=models.CASCADE, related_name='users', null=True)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.GUEST
    )
    objects = CustomUserManager()

    class Meta:
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def to_entity(self):
        return User(
            name=self.get_full_name(),
            role=UserRoleEntity.get(self.role),
            city=self.city.to_entity(),
            id=self.pk
        )

    def __str__(self):
        return f"{self.get_full_name()}"