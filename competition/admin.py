from django.contrib import admin
from .models import *
class CompetitionImageInline(admin.TabularInline):
    model = CompetitionImage
    extra = 1  # Number of extra forms to display for adding new images

class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionImageInline]

admin.site.register(Competition)
admin.site.register(HolidayCompetition)
admin.site.register(Entry)
admin.site.register(Winner)
admin.site.register(BasketItem)
admin.site.register(MpesaTransaction)
admin.site.register(Ticket)
admin.site.register(CompetitionImage)
