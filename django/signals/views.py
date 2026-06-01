from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from signals import _services as _svc
from signals.serializers import (
    CreateSignalSerializer,
    RiskSummarySerializer,
    SignalResponseSerializer,
)


class SignalIngestView(APIView):
    # SRP: only handles signal ingestion requests — risk scoring is a separate view
    authentication_classes = []
    permission_classes = []

    def post(self, request: Request) -> Response:
        ser = CreateSignalSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        saved = _svc.ingestion.ingest(ser.validated_data)
        return Response(SignalResponseSerializer(saved).data, status=201)


class RiskSummaryView(APIView):
    # SRP: only handles risk summary reads — signal writes are a separate view
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request, service_name: str) -> Response:
        summary = _svc.risk.get_risk_summary(service_name)
        return Response(RiskSummarySerializer(summary).data, status=200)
