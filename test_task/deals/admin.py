from deals.models import Deal, Gem
from django.contrib import admin


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    pass


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    pass
