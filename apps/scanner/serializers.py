from rest_framework import serializers
from .models import ScanSession


class ScanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanSession
        fields = ['image']


class ScanResultSerializer(serializers.ModelSerializer):
    is_genuine = serializers.BooleanField(read_only=True)

    class Meta:
        model = ScanSession
        fields = [
            'id',
            'image',
            'heatmap',
            'status',
            'result',
            'mse_score',
            'threshold',
            'confidence',
            'is_genuine',
            'created_at',
        ]