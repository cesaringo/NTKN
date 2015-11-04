from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.html import format_html
from django.conf.urls.static import static


class Photo(models.Model):
    original = models.ImageField(upload_to='account_photos')
    thumbnail_30x30 = ImageSpecField(source='original', processors=[ResizeToFill(30, 30)], format='JPEG',
                                     options={'quality': 100})
    thumbnail_50x50 = ImageSpecField(source='original', processors=[ResizeToFill(50, 50)], format='JPEG',
                                     options={'quality': 100})
    thumbnail_100x100 = ImageSpecField(source='original', processors=[ResizeToFill(100, 100)], format='JPEG',
                                       options={'quality': 100})

    def __str__(self):
        return self.original.name


class AccountManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """Creates and saves a User with the given username, email and password."""
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        account = self.model(username=username, email=email, **extra_fields)
        account.set_password(password)
        account.save()
        return account

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.set_default('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AccountManager()
    is_active = models.BooleanField(default=True)
    photo = models.OneToOneField(Photo, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def get_photo_as_tag(self):
        if self.photo:
            return format_html('<img src="{}" alt="{}">',
                               self.photo.thumbnail_30x30.url, self.__unicode__())
        else:
            return None

    def __str__(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.__str__()

    get_photo_as_tag.allow_tags = True

    def email_link(self):
        return format_html('<a href="mailto:{}">{}</a>', self.email, self.email)

    email_link.allow_tags = True
