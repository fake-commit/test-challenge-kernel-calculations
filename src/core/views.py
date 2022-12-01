from core.serializers import (
    KernelCalculationSerializer,
    KernelCalculationsSerializer,
    KernelCalculationRequestSerializer,
)
from core.tasks import calculate_kernel_results
from django_celery_results.models import TaskResult
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


class KernelCalculationViewSet(ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = [
        "date_created",
    ]
    lookup_field = "task_id"

    def get_serializer_class(self):
        if self.action == "list":
            return KernelCalculationsSerializer
        if self.action == "retrieve":
            return KernelCalculationSerializer


class KernelCalculateView(CreateAPIView):
    serializer_class = KernelCalculationRequestSerializer

    def create(self, request, *args, **kwargs):
        request_data_serializer = self.serializer_class(data=request.data)
        request_data_serializer.is_valid(raise_exception=True)
        async_result = calculate_kernel_results.delay(**request_data_serializer.data)
        return Response({"task_id": async_result.id})
