from .models import Memo, Url
from rest_framework import serializers

class MemoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    deleted_at = serializers.DateTimeField(write_only=True, required=False)

    class Meta:
        model = Memo
        fields = '__all__'


class UrlSerializer(serializers.ModelSerializer):
    memo = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = Url
        fields = '__all__'
