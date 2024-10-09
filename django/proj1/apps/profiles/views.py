import json
from django.db.models.query_utils import logging
from django.http import JsonResponse
from .models import Profile

def get(request):
    try:
        profiles = Profile.objects.all().values('id', 'first_name', 'last_name', 'profession', 'type')
        csrf_token = request.COOKIES.get('csrftoken')
        print("csrf_token: ", csrf_token)
        return JsonResponse(list(profiles), safe=False)
    except Exception as e:
        logging.error(str(e))
        return JsonResponse({'error': str(e)}, status=500)


def post(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)

            Profile.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                profession=data['profession'],
                type=data['type'],
                user_id=data['user_id']
            )

            return JsonResponse({}, status=201)
    except Exception as e:
        logging.error("Error: ", str(e))
        return JsonResponse({'error': str(e)}, status=500)


