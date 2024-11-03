from django.contrib import admin
from .models import Messages, Room, Topics, User

admin.site.register(Messages)
admin.site.register(Room)
admin.site.register(Topics)
admin.site.register(User)