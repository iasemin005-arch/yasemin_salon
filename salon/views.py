from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json
from .models import Service, Master, GalleryPhoto, Review, Appointment


def home(request):
    services = Service.objects.filter(is_active=True)
    masters = Master.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_approved=True)[:6]
    gallery = GalleryPhoto.objects.filter(is_active=True)[:12]
    categories = Service.CATEGORY_CHOICES
    context = {
        'services': services,
        'masters': masters,
        'reviews': reviews,
        'gallery': gallery,
        'categories': categories,
        'services_by_category': {
            cat[0]: services.filter(category=cat[0]) for cat in categories
        },
    }
    return render(request, 'salon/home.html', context)


def get_services_json(request):
    services = list(Service.objects.filter(is_active=True).values('id', 'name', 'category', 'price', 'duration'))
    return JsonResponse({'services': services})


def get_masters_json(request):
    masters = list(Master.objects.filter(is_active=True).values('id', 'name', 'specialty'))
    return JsonResponse({'masters': masters})


@require_POST
def book_appointment(request):
    try:
        data = json.loads(request.body)
        service_id = data.get('service_id')
        master_id = data.get('master_id')
        appt = Appointment(
            client_name=data['client_name'],
            client_phone=data['client_phone'],
            client_email=data.get('client_email', ''),
            date=data['date'],
            time=data['time'],
            comment=data.get('comment', ''),
            payment_method=data.get('payment_method', 'cash'),
        )
        if service_id:
            try:
                appt.service = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                pass
        if master_id:
            try:
                appt.master = Master.objects.get(id=master_id)
            except Master.DoesNotExist:
                pass
        appt.save()
        return JsonResponse({'success': True, 'message': 'Запись успешно создана! Мы свяжемся с вами для подтверждения.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Ошибка: {str(e)}'}, status=400)


@require_POST
def submit_review(request):
    try:
        data = json.loads(request.body)
        review = Review(
            client_name=data['client_name'],
            rating=int(data.get('rating', 5)),
            text=data['text'],
        )
        service_id = data.get('service_id')
        if service_id:
            try:
                review.service = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                pass
        review.save()
        return JsonResponse({'success': True, 'message': 'Спасибо за отзыв! Он будет опубликован после проверки.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
