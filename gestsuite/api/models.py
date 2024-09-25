from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .validations import validate_rut

class AppUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('El email es obligatorio.')
		if not username:
			raise ValueError('El nombre de usuario es obligatorio.')
		if not password:
			raise ValueError('La contraseña es obligatoria.')
		email = self.normalize_email(email)
		user = self.model(username=username, email = email)
		user.set_password(password)
		user.save()
		return user
	
	def create_superuser(self, username, email, password=None):
		if not email:
			raise ValueError('El email es obligatorio.')
		if not username:
			raise ValueError('El nombre de usuario es obligatorio.')
		if not password:
			raise ValueError('La contraseña es obligatoria.')
		
		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(max_length=50, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	
	objects = AppUserManager()
	
	def __str__(self):
		return self.username

