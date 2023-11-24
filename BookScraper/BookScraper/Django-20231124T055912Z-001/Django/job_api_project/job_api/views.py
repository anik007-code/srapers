import json
import redis
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# job_api/views.py

@csrf_exempt
def create_job(request):
    if request.method == 'POST':
        try:
            job_data = json.loads(request.body.decode('utf-8'))

            # Validate the required fields
            required_fields = ['name', 'price', 'stock', 'html_structure']
            for field in required_fields:
                if field not in job_data:
                    return JsonResponse({"error": f"Missing required field: {field}"}, status=400)

            # redis_conn = redis.Redis(host='localhost', port=6379, db=0)
            # Process and store the job data in Redis as a JSON string in the list
            redis_conn = redis.Redis(host='localhost', port=6379, db=0)
            job_data_json = json.dumps(job_data)
            redis_conn.rpush('job_data_list', job_data_json)

            return JsonResponse({"message": "Job created successfully"}, status=201)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"Invalid JSON format: {str(e)}"}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


def index(request):
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    job_data_list = redis_conn.lrange('Books', 0, -1)

    jobs_data = [json.loads(job_data) for job_data in job_data_list]

    context = {
        'jobs_data': jobs_data,
    }

    return render(request, 'job_api/index.html', context)
