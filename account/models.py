import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Custom User Manager

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None, user_type="operator"):
        """
        Creates and saves a User with the given email, name, password and user_type.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, user_type="owner"):
        """
        Creates and saves a superuser with the given email, name, password and user_type.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            user_type=user_type,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


# Custom User Model

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    user_type = models.CharField(max_length=10, choices=[('owner', 'Owner'), ('operator', 'Operator')],
                                 default="operator")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_type']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine_name = models.CharField(max_length=255, default=None)
    mac_address = models.CharField(max_length=255, default=None)
    status_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_status = models.DateTimeField(auto_now=True)


class Scan(models.Model):
    scan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    predict_value = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ScanData(models.Model):
    user_connection = models.ForeignKey(UserConnection, on_delete=models.CASCADE, related_name='user_connection')
    scan_connection = models.ForeignKey(Scan, on_delete=models.CASCADE,  related_name='scan_connection')
    energy = models.FloatField()
    wavelength = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
