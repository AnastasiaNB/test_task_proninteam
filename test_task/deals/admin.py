from django.contrib import admin

from deals.models import Gem, Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    pass


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    pass
