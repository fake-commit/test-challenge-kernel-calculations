from core.kernel import main
from core.serializers import KernelCalculationResultSerializer

from celery import shared_task


@shared_task
def calculate_kernel_results(date_start, date_fin, lag):

    calculation_results_serializer = KernelCalculationResultSerializer(
        data=main(date_start, date_fin, lag).to_dict("records"), many=True
    )
    calculation_results_serializer.is_valid(raise_exception=True)
    return calculation_results_serializer.data
