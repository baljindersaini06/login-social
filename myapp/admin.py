from django.contrib.auth.models import Permission
from django.contrib import admin
from myapp.models import *
admin.site.register(Permission)
# Register your models here.
admin.site.register(User)
admin.site.register(SiteConfiguration)
admin.site.register(SmtpConfiguration)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(WebsiteType)
admin.site.register(Website)
admin.site.register(Location)

admin.site.register(LicenceType)
admin.site.register(Licence)

admin.site.register(Document_category)
admin.site.register(Documents)
admin.site.register(Document_File)
admin.site.register(Document_Links)



admin.site.register(Package)
admin.site.register(Company_package)

admin.site.register(DeviceType)
admin.site.register(Device)


admin.site.register(Meeting)
