from django.contrib import admin

from .models import Logwork, Furnace, Furnacework, Setusertemp, Settings

class FurnaceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['work']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('work', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['work']

class FurnaceworkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['temp']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('temp', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['temp']
    
class SetusertempAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['usertemp']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('usertemp', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['usertemp']
    
admin.site.register(Furnace, FurnaceAdmin)
admin.site.register(Furnacework, FurnaceworkAdmin)
admin.site.register(Setusertemp, SetusertempAdmin)
admin.site.register(Settings)
