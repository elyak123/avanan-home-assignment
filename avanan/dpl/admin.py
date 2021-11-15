from django.contrib import admin
from avanan.dpl.models import Leak, Pattern


class LeakAdmin(admin.ModelAdmin):
    pass


class PatternAdmin(admin.ModelAdmin):
    pass


admin.site.register(Leak, LeakAdmin)
admin.site.register(Pattern, PatternAdmin)
