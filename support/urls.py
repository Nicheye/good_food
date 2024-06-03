from django.urls import path
from .views import Report_View,Ticket_View,admin_dashboard,respond_report,respond_ticket

urlpatterns = [
    path('report/',Report_View.as_view(),name="report_lists"),
    path('report/<int:id>/',Report_View.as_view(),name="report_item"),
    path('ticket/',Ticket_View.as_view(),name="ticket_lists"),
    path('ticket/<int:id>/',Ticket_View.as_view(),name="ticket_item"),
    path('dash/', admin_dashboard, name='admin_dashboard'),
    path('respond-report/<int:report_id>/', respond_report, name='respond_report'),
    path('respond-ticket/<int:ticket_id>/', respond_ticket, name='respond_ticket'),
]
