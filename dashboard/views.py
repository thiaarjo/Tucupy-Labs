from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import User
from credits.models import CarbonCredit, CreditListing
from transactions.models import Transaction
from django.contrib.auth import login

@login_required
def index(request):
    user = request.user
    
    if user.role == User.Roles.PRODUCER:
        # Dados para PRODUTOR
        context = {
            'available_credits': CarbonCredit.objects.filter(owner=user, status='AVAILABLE').count(),
            'listed_credits': CarbonCredit.objects.filter(owner=user, status='LISTED').count(),
            'sold_credits': CarbonCredit.objects.filter(owner=user, status='SOLD').count(),
            'total_credits': CarbonCredit.objects.filter(owner=user).count(),
            'recent_sales': Transaction.objects.filter(seller=user).order_by('-timestamp')[:5],
        }
        return render(request, "dashboard/producer.html", context)
    
    elif user.role == User.Roles.COMPANY:
        # Dados para EMPRESA
        context = {
            'purchased_credits': Transaction.objects.filter(buyer=user).count(),
            'total_investment': sum([t.total_price for t in Transaction.objects.filter(buyer=user)]),
            'recent_purchases': Transaction.objects.filter(buyer=user).order_by('-timestamp')[:5],
        }
        return render(request, "dashboard/company.html", context)
    
    elif user.role == User.Roles.ADMIN:
        # Dados para ADMIN
        context = {
            'total_users': User.objects.count(),
            'total_transactions': Transaction.objects.count(),
            'total_credits': CarbonCredit.objects.count(),
        }
        return render(request, "dashboard/admin.html", context)
    
    else:
        return render(request, "dashboard/index.html", {})

def create_test_users(request):
    # Cria usuário PRODUCER
    producer = User.objects.create_user(
        username='producer1', 
        password='123', 
        role=User.Roles.PRODUCER
    )
    
    # Cria usuário COMPANY  
    company = User.objects.create_user(
        username='company1',
        password='123',
        role=User.Roles.COMPANY
    )
    
    # Faz login como producer
    login(request, producer)
    return HttpResponse("Usuários criados! Logado como producer1")