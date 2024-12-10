from rest_framework import serializers
from .models import SearchDomain


class SearchDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDomain
        fields = "__all__"

# Create 전용 Serializer
class CreateSearchDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDomain
        # POST 요청 시 필요한 필드만 포함
        fields = ["domain_column", "value"]  # 예시로 'name'과 'description'만 포함

    def validate_name(self, value):
        """name 필드에 대한 추가 검증 로직"""
        if len(value) < 3:
            raise serializers.ValidationError("The name must be at least 3 characters long.")
        return value

    def create(self, validated_data):
        """객체 생성 로직을 커스터마이징할 경우"""
        method = self.context['request'].method
        headers = self.context['request'].headers
        path = self.context['request'].path
        query_params = self.context['request'].query_params
        print("jinha", method,headers, path, query_params)
        # 예: 추가적으로 `owner` 필드에 현재 사용자를 할당
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)