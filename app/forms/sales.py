from django.forms import ModelForm
from app.models import Sale

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'
