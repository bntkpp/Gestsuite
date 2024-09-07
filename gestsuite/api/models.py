from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class AppUserManager(BaseUserManager):
	def create_user(self, username, password=None):
		if not username:
			raise ValueError('El nombre de usuario es obligatorio.')
		if not password:
			raise ValueError('La contraseña es obligatoria.')
		user = self.model(username=username)
		user.set_password(password)
		user.save()
		return user
	
	def create_superuser(self, username, password=None):
		if not username:
			raise ValueError('El nombre de usuario es obligatorio.')
		if not password:
			raise ValueError('La contraseña es obligatoria.')
		user = self.create_user(username, password)
		user.is_superuser = True
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(max_length=50, unique=True)
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	
	objects = AppUserManager()
	
	def __str__(self):
		return self.username

