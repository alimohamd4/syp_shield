from rest_framework import serializers
from .models import ScanSession


class ScanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ScanSession
        fields = ['image']


class ScanResultSerializer(serializers.ModelSerializer):
    is_genuine      = serializers.BooleanField(read_only=True)
    heatmap_url     = serializers.SerializerMethodField()

    class Meta:
        model  = ScanSession
        fields = [
            'id', 'image', 'heatmap', 'heatmap_url',
            'status', 'result', 'mse_score',
            'threshold', 'confidence', 'is_genuine',
            'notes', 'created_at',
        ]

    def get_heatmap_url(self, obj):
        if obj.heatmap:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.heatmap.url)
        return None