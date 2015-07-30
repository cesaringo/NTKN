from django.contrib import admin
from authentication.models import Account, Photo
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _


class AccountAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
		                             'groups', 'user_permissions')}),
		#(_('Important dates'), {'fields': ('last_login', 'created_at')}),
	)
	pass

admin.site.register(Account, AccountAdmin)
admin.site.register(Photo)
# Register your models here.
	