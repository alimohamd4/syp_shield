from rest_framework import generics, permissions, status
from core.responses import ApiResponse, get_lang
from core.messages import get_message
from .models import ScanSession
from .serializers import ScanCreateSerializer, ScanResultSerializer


class ScanCreateView(generics.CreateAPIView):
    serializer_class = ScanCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        scan = serializer.save(user=self.request.user, status='processing')
        self._run_inference(scan)

    def _run_inference(self, scan):
        scan.status = 'completed'
        scan.result = 'genuine'
        scan.mse_score = 0.00320
        scan.confidence = 95.5
        scan.save()

    def create(self, request, *args, **kwargs):
        lang = get_lang(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        scan = ScanSession.objects.filter(
            user=request.user,
            status='completed'
        ).latest('created_at')
        result_serializer = ScanResultSerializer(scan)
        return ApiResponse.created(
            data=result_serializer.data,
            message_key='scan_success',
            lang=lang
        )


class ScanHistoryView(generics.ListAPIView):
    serializer_class = ScanResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScanSession.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        lang = get_lang(request)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(
            data=serializer.data,
            message_key='scan_history',
            lang=lang
        )


class ScanDetailView(generics.RetrieveAPIView):
    serializer_class = ScanResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScanSession.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        lang = get_lang(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(
            data=serializer.data,
            message_key='success',
            lang=lang
        )