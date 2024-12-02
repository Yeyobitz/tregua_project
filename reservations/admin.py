from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_active')
    list_filter = ('is_active', 'capacity')
    search_fields = ('number',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code', 'customer_name', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'table')
    search_fields = ('customer_name', 'customer_email', 'confirmation_code')
    readonly_fields = ('confirmation_code', 'created_at', 'updated_at')
