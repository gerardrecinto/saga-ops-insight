from django.urls import path

from signals.views import RiskSummaryView, SignalIngestView

urlpatterns = [
    path("signals", SignalIngestView.as_view()),
    path("services/<str:service_name>/risk-summary", RiskSummaryView.as_view()),
]
