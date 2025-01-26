from django.contrib import admin
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from allauth.socialaccount.admin import SocialTokenAdmin as BaseSocialTokenAdmin
from allauth.socialaccount.admin import SocialAccountAdmin as BaseSocialAccountAdmin
from allauth.socialaccount.admin import SocialAppAdmin as BaseSocialAppAdmin

class SocialTokenAdmin(BaseSocialTokenAdmin):
    compressed_fields = []

class SocialAccountAdmin(BaseSocialAccountAdmin):
    compressed_fields = []

class SocialAppAdmin(BaseSocialAppAdmin):
    compressed_fields = []

# Unregister the default admin classes
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)

# Register our custom admin classes
admin.site.register(SocialToken, SocialTokenAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(SocialApp, SocialAppAdmin)

# Register your models here.
