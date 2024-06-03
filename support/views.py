from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReportResponseForm, TicketResponseForm

class Report_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user = request.user
        id = kwargs.get("id",None)
        if id is None:
            reports_query = Report.objects.filter(created_by=user)
            reports_ser = Report_Serializer(reports_query,many=True)
            return Response({'data':reports_ser.data},status=status.HTTP_200_OK)
        report_obj = Report.objects.get(id=id)
        if report_obj.created_by !=user:
            return Response({'message':'you are not allowed to see not yours reports'},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        user =request.user
        data = request.data
        report_ser = Report_Serializer(data=data)
        report_ser.is_valid(raise_exception=True)
        report_ser.save()
        return Response({'data':report_ser.data},status=status.HTTP_201_CREATED)
    
class Ticket_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user = request.user
        id = kwargs.get("id",None)
        if id is None:
            tickets_query = Ticket.objects.filter(created_by=user)
            tickets_ser = Ticket_Serializer(tickets_query,many=True)
            return Response({'data':tickets_ser.data},status=status.HTTP_200_OK)
        ticket_obj = Ticket.objects.get(id=id)
        if ticket_obj.created_by !=user:
            return Response({'message':'you are not allowed to see not yours ticket'},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        user =request.user
        data = request.data
        ticket_ser = Ticket_Serializer(data=data)
        ticket_ser.is_valid(raise_exception=True)
        ticket_ser.save()
        return Response({'data':ticket_ser.data},status=status.HTTP_201_CREATED)


def admin_dashboard(request):
    pending_reports = Report.objects.filter(status='pending')
    pending_tickets = Ticket.objects.filter(status='pending')
    return render(request, 'tic_rep_admin.html', {
        'pending_reports': pending_reports,
        'pending_tickets': pending_tickets
    })

def respond_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        form = ReportResponseForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ReportResponseForm(instance=report)
    return render(request, 'respond_report.html', {'form': form})

def respond_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketResponseForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = TicketResponseForm(instance=ticket)
    return render(request, 'respond_ticket.html', {'form': form})
