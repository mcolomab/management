from decimal import Decimal

from django.contrib import admin
from .models import Partner, Product, MaterialList, Component, Document, Purchase, PurchaseDetail, Inventory


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type', 'document_number', 'partner_type')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'current_number')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('movement_type', 'product', 'quantity', 'date')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('stock',)
    list_display = ('name', 'stock', 'terminado_o_insumo')

class ComponentInline(admin.TabularInline):
    model = Component

@admin.register(MaterialList)
class MaterialListAdmin(admin.ModelAdmin):
    inlines = [ComponentInline,]

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseDetailInline,]
    readonly_fields = (
        'document_number',
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
    def response_add(self, request, new_object):
        doc = new_object.document_type
        new_object.document_number = doc.serial + '-' + str(doc.current_number)
        doc.current_number += 1
        doc.save()
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super(PurchaseAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super(PurchaseAdmin, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):
        sub_total, igv, recibida = Decimal(0), Decimal(0), False
        for item in obj.purchase_details.all():
            if obj.document_type.abbreviation.lower() == 'fac':
                sub_total += item.quantity * item.unit_price * Decimal(1 - (item.discount/100))
                igv += item.quantity * item.unit_price * Decimal(0.18)
            elif obj.document_type.abbreviation.lower() == 'bol':
                sub_total += item.quantity * item.unit_price * Decimal(0.18) * Decimal(1 - (item.discount/100))
                igv = Decimal(0)
            else:
                sub_total += item.quantity * item.unit_price * Decimal(1 - (item.discount/100))
                igv = Decimal(0)

            obj.sub_total = sub_total
            obj.igv = igv
            obj.total = sub_total + igv

            if obj.status == 'confirmada':
                Inventory.objects.create(
                    movement_type='compra',
                    product=item.product,
                    quantity=item.quantity,
                    document=obj.document_type.abbreviation+obj.document_number
                )
                recibida = True

        if recibida:
            obj.status = 'recibida'

        TWOPLACES = Decimal(10) ** -2
        if obj.amount_paid == Decimal(obj.total).quantize(TWOPLACES):
            obj.status = 'pagada'
        obj.save()
        return obj

