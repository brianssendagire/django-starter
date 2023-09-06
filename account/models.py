import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class BaseAccountManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, phone_number='0417801038', image='default', password=None):
        if not username:
            raise ValueError('A valid username is required')
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Please tell us your first name')
        if not last_name:
            raise ValueError('Please tell us your last name')
        if not phone_number:
            raise ValueError('Phone number is required')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            phone_number=phone_number
        )
        user.image = image
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name,
                         phone_number='0417801038',
                         image='default', password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            first_name=first_name.title(),
            last_name=last_name.title(),
            phone_number=phone_number
        )
        user.image = image
        user.is_admin = True
        user.is_manager = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename):
    file_path = 'faces/{name}/{filename}'.format(
        name=str(instance.first_name).split()[0], filename=filename)
    return file_path


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="Username", max_length=360, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=1000, null=True, blank=True, default='Kampala, UGANDA')
    phone_number = models.CharField(max_length=100, null=True, blank=True, default='0414251064')
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    last_access = models.DateTimeField(verbose_name='Last Access', null=True, blank=True)
    leave_update_date = models.DateTimeField(null=True, blank=True, verbose_name="Leave Update Date")
    password_updated = models.DateTimeField(null=True, blank=True, verbose_name="Password Updated on")
    password_changed = models.BooleanField(default=False)

    is_manager = models.BooleanField(default=False)
    is_professional = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    objects = BaseAccountManager()

    def __str__(self):
        return "{} {}".format(str(self.first_name), str(self.last_name))

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_delete, sender=Account)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Account` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Account)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Account` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Account.objects.get(pk=instance.pk).image
        new_file = instance.image
        if old_file and new_file:
            if not old_file == new_file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
    except Account.DoesNotExist:
        pass
