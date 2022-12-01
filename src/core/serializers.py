import json

from django_celery_results.models import TaskResult
from rest_framework import serializers


class KernelCalculationRequestSerializer(serializers.Serializer):
    date_start = serializers.DateField(required=True)
    date_fin = serializers.DateField(required=True)
    lag = serializers.IntegerField(required=True)

    def validate(self, data):
        if data["date_start"] > data["date_fin"]:
            raise serializers.ValidationError(
                {
                    "date_start": "Please enter a valid date_start, should be less than date_fin.",
                    "date_fin": "Please enter a valid date_fin, should be greater than date_start.",
                }
            )
        return data


class KernelCalculationResultSerializer(serializers.Serializer):
    date = serializers.DateTimeField(required=True)
    liquid = serializers.FloatField(required=True)
    oil = serializers.FloatField(required=True)
    water = serializers.FloatField(required=True)
    wct = serializers.FloatField(required=True)


class KernelCalculationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = (
            "task_id",
            "status",
            "date_created",
            "date_done",
        )


class KernelCalculationSerializer(serializers.ModelSerializer):

    result = serializers.SerializerMethodField()
    calculation_time = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(KernelCalculationSerializer, self).__init__(*args, **kwargs)
        field_names = self.context['request'].query_params.get('fields', '').split(',')
        optional = getattr(self.Meta, 'optional', None)
        for field_name in optional:
            if field_name not in field_names:
                self.fields.pop(field_name, '')

    def get_calculation_time(self, obj):
        return obj.date_done - obj.date_created

    def get_result(self, obj):
        if obj.status not in ["SUCCESS", "FAILED"]:
            return None
        result_data = json.loads(obj.result)
        if isinstance(result_data, list):
            result_serializer = KernelCalculationResultSerializer(data=result_data, many=True)
            result_serializer.is_valid()
            return result_serializer.data
        return result_data

    class Meta:
        model = TaskResult
        fields = (
            "task_id",
            "status",
            "result",
            "calculation_time"
        )
        optional = (
            "calculation_time",
        )
