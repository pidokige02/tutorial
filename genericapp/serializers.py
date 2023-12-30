from rest_framework import serializers
from genericapp.models import SearchDomain


class SearchDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDomain
        fields = "__all__"
