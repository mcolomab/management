from django.forms import inlineformset_factory
from django.shortcuts import render
from app.models import Sale, SaleDetail
from app.forms import SaleForm

def viewsale(request):
    form = SaleForm()
    SaleDetailInlineFormSet = inlineformset_factory(
        Sale,
        SaleDetail,
        fields=('product', 'quantity', 'unit_price', 'discount',),
        extra=1
    )
    formset = SaleDetailInlineFormSet()
    return render(request, 'sales/sale.html', {'formset': formset, 'form': form})