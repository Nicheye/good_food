from authentification.models import Profile
from django.utils import timezone
from datetime import timedelta
from authentification.models import User
from .models import Payment
from celery import shared_task

@shared_task
def check_current_premium():
    # Calculate the date 30 days ago from now
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Get all users and prefetch their profiles to reduce database hits
    users = User.objects.select_related('profile').all()

    # Collect the users who need their profile updated
    users_to_update = []

    for user in users:
        # Filter payments for the user made in the last 30 days
        payment_exists = Payment.objects.filter(user=user, created_at__gte=thirty_days_ago,status="approved").exists()
        
        if payment_exists:
            if user.profile.account_type != 'premium':
                user.profile.account_type = 'premium'
                users_to_update.append(user.profile)
        else:
            print(f"User {user.username} has not made a payment in the last 30 days.")

    # Bulk update the profiles
    if users_to_update:
        Profile.objects.bulk_update(users_to_update, ['account_type'])

