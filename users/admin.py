from django.contrib import admin

from users.models import NewUser, Consultant, Customer

# Register your models here.
admin.site.register(NewUser)
admin.site.register(Consultant)
admin.site.register(Customer)