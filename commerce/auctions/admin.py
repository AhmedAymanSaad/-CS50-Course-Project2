from django.contrib import admin
from .models import Listing, Comments, Bid, User, WatchList

class ListingAdmin(admin.ModelAdmin):
    fields = (('description', 'title'), 'image')

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(WatchList)
admin.site.register(User)