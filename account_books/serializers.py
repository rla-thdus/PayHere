from .models import Memo
from rest_framework import serializers

class MemoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    deleted_at = serializers.DateTimeField(write_only=True, required=False)

    class Meta:
        model = Memo
        fields = '__all__'
