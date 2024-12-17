import json
import io
from openpyxl import Workbook
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.utils import timezone
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


def generate_excel(request):

    print("01")
    wb = Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    robots = Robot.objects.filter(created__gte=one_week_ago)

    robot_counts = {}

    for robot in robots:
        model = robot.model
        version = robot.version
        key = (model, version)

        if model not in robot_counts:
            robot_counts[model] = {}
        if version not in robot_counts[model]:
            robot_counts[model][version] = 0

        robot_counts[model][version] += 1

    for model, versions in robot_counts.items():
        ws = wb.create_sheet(title=f"Model_{model}")
        ws.append(['Model', 'Version', 'Quantity'])

        for version, count in versions.items():
            ws.append([model, version, count])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="robot_production_report.xlsx"'

    wb.save(response)
    return response

