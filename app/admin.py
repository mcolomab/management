from decimal import Decimal

from django.contrib import admin, messages
from .models import (Document, Inventory, Partner, ProductionOrder,
                    Product, Purchase, PurchaseDetail, Component,
                    MaterialList, Sale, SaleDetail)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'current_number')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('movement_type', 'product', 'quantity', 'date')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type', 'document_number', 'partner_type')

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('document_number',)
    list_display = (
        'document_number',
        'date',
        'material_list', 
        'quantity_to_produce',
        'status',
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('stock',)
    list_display = ('name', 'stock', 'terminado_o_insumo')

@admin.register(PurchaseDetail)
class PurchaseDetailAdmin(admin.ModelAdmin):
    pass

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseDetailInline,]
    readonly_fields = (
        'sub_total',
        'igv',
        'total',
    )
    list_display = (
        'document_number',
        'document_type',
        'provider',
        'total',
        'amount_paid',
        'status',
    )

class ComponentInline(admin.TabularInline):
    model = Component

@admin.register(MaterialList)
class MaterialListAdmin(admin.ModelAdmin):
    inlines = [ComponentInline,]

@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    pass

class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleDetailInline,]
    readonly_fields = (
        'document_number',
        'sub_total',
        'igv',
        'total',
    )
    list_display = (
        'document_number',
        'document_type',
        'customer',
        'total',
        'amount_paid',
        'status',
    )
