import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Robot

@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data, "_____DATA")

            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            if not model or not version or not created:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if len(model) > 2:
                return JsonResponse({'error': 'Model field exceeds maximum length of 2'}, status=400)
            if len(version) > 2:
                return JsonResponse({'error': 'Version field exceeds maximum length of 2'}, status=400)

            created_date = parse_datetime(created)
            if created_date is None:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

            if Robot.objects.filter(model=model, version=version, created=created_date).exists():
                return JsonResponse({'error': 'Robot with these details already exists'}, status=400)

            robot = Robot.objects.create(
                model=model,
                version=version,
                created=created_date
            )

            return JsonResponse({'message': 'Robot created successfully', 'id': robot.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
