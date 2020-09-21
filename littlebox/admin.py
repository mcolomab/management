from django.contrib import admin

from .models import LittleBox, LittleBoxMovement

@admin.register(LittleBox)
class LittleBoxAdmin(admin.ModelAdmin):
    actions = 'cerrar_caja'

    def cerrar_caja(self, request, queryset):
        for q in queryset:
            q.cerrar()
    cerrar_caja.short_description = "Cerrar caja"

@admin.register(LittleBoxMovement)
class LittleBoxMovementAdmin(admin.ModelAdmin):
    pass