from rest_framework import generics

from app.models import Partner
from app.serializers import PartnerSerializer

class CustomerList(generics.ListCreateAPIView):
    queryset = Partner.objects.filter(partner_type='customer')
    serializer_class = PartnerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer