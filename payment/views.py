from django.http import JsonResponse, HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

@csrf_exempt
def mpesa_stk_push(request):
    if request.method == 'POST':
        phone_number = request.POST.get('booking_email_or_phone')
        mpesa_client = MpesaClient()
        callback_url = 'https://e22e-154-159-237-48.ngrok-free.app'  
        response = mpesa_client.stk_push(phone_number, 1, 'NextGen Payment', 'Payment for booking', callback_url)
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def mpesa_confirmation(request):
    if request.method == 'POST':
        mpesa_body = request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)
        print(mpesa_payment)  

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def mpesa_validation(request):
    if request.method == 'POST':
        # Parse incoming JSON data from M-Pesa
        data = json.loads(request.body.decode('utf-8'))
        response = {
            "ResultCode": 0,
            "ResultDesc": "Validation request received successfully"
        }
        return HttpResponse(json.dumps(response), content_type='application/json')

    return HttpResponse(status=405)  