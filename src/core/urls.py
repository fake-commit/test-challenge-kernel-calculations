from core.views import KernelCalculateView, KernelCalculationViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("kernel/calculate/", KernelCalculateView.as_view(), name="calculate"),
]

router = DefaultRouter()
router.register("kernel/calculations", KernelCalculationViewSet)
urlpatterns += router.urls
