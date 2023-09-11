from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from .models import Submission, Grading, AccessCode
from django.views import View

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def entry_submission(request):
  state_of_orgin = Submission.NIGERIAN_STATES
  document_type = Submission.DOCUMENT_TYPES
  current_date = datetime.now().date()
  submission_expiry_date = datetime(2023, 9, 12).date()
  context = {
       'current_date':current_date,
       'submission_expiry_date':submission_expiry_date,
       'state_of_orgin':state_of_orgin,
       'document_type':document_type,
  }
  return render(request, 'entry_submission.html', context)

class UploadFileView(View):
    def post(self, request, *args, **kwargs):
        try:
            name = request.POST['name']
            phone_number = request.POST['phone_number']
            age_range = request.POST['age_range']
            state_of_origin = request.POST['state_of_origin']
            educational_institution = request.POST['educational_institution']
            current_level = request.POST['current_level']
            document_type = request.POST['document_type']
            uploaded_file = request.FILES['uploaded_file']
        except KeyError:
            return JsonResponse({'error': 'No file was uploaded.'}, status=400)
        
        # Get the title and description from the form data
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        age_range = request.POST['age_range']
        state_of_origin = request.POST['state_of_origin']
        educational_institution = request.POST['educational_institution']
        current_level = request.POST['current_level']
        uploaded_file = request.FILES['uploaded_file']
        document_type = request.POST['document_type']

        entry_save = Submission(
            name=name,
            phone_number=phone_number,
            age_range=age_range,
            state_of_origin=state_of_origin,
            educational_institution=educational_institution,
            current_level=current_level,
            document_type = document_type,
        )
        entry_save.attachment.save(uploaded_file.name, uploaded_file, save=True)
        entry_save.save()

        response_data = {
            'message': f'Entry submitted successfully. Your ID: {entry_save.auto_id} *Please Copy and Keep Your ID Safe*'
        }

        return JsonResponse(response_data)
    
def view_submission(request, auto_id):
    submission = get_object_or_404(Submission, auto_id=auto_id)
    grading = Grading.objects.filter(submission=submission)
    context = {
        'submission': submission,
        'grading':grading,
      }
    return render(request, 'view.html', context)
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

def admin_dashboard(request):
    # Retrieve all submissions from the database
    submissions = Submission.objects.all()
    
    # Pagination
    page_number = request.GET.get('page')
    items_per_page = 10  # You can adjust the number of items per page as needed
    paginator = Paginator(submissions, items_per_page)
    page = paginator.get_page(page_number)
    
    # Initialize the query variable
    query = request.GET.get('q')
    
    if query:
            submissions = submissions.filter(
                Q(name__icontains=query) |
                Q(auto_id__icontains=query)
            )
        
    
    submissions_count = submissions.count()
    judges = AccessCode.objects.all().count()

    context = {
        'submissions': page,
        'submissions_count': submissions_count,
        'judges': judges,
        'query': query,  # Pass the query back to the template for displaying in the search input
    }

    return render(request, 'admin_dashboard.html', context)



def admin_view_submission(request, auto_id):
    
    submission = get_object_or_404(Submission, auto_id=auto_id)
    submissions = Submission.objects.all()
    grading = Grading.objects.filter(submission=submission)
    submissions_count = submissions.count()
    judges = AccessCode.objects.all().count()
    context = {
        'submission':submission,
        'submissions': submissions,
        'submissions_count':submissions_count,
        'judges':judges,
        'grading':grading,
      }
    return render(request, 'admin_view_submission.html', context)

from django.http import JsonResponse
import json

def grade_submission(request):
    if request.method == 'POST':
        auto_id = request.POST.get('auto_id')
        submission = get_object_or_404(Submission,auto_id=auto_id)
        grader = request.POST.get('grader')
        grade = request.POST.get('grade')
        feedback = request.POST.get('feedback')

        Grading.objects.create(grade=grade, feedback=feedback, submission=submission, grader=grader)
        submission.grade +=int(grade)
        submission.save()
        # Process and save grading data here (e.g., create a Grading model instance)

        # Return a JSON response to indicate success
        return JsonResponse({"success": True, "message": "Grading submitted successfully."})
    # Handle GET requests or other cases
    return JsonResponse({'message': 'Invalid request method'}, status=400)


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .models import AccessCode



def enter_access_code(request):
    if request.method == 'POST':
        code = request.POST.get('access_code')
        try:
            access_code = AccessCode.objects.get(code=code, used=False)
            access_code.used = True
            access_code.save()
            dashboard_url = '/dashboard/'  # Replace this with your actual dashboard URL
            link_to_dashboard = f'<a href="{dashboard_url}">Go to Dashboard</a>'
            response_content = f"Access granted. {link_to_dashboard}"
            response = HttpResponse(response_content) # Set a cookie to remember the code
            
            # Create a dictionary to store the data you want in the cookie
            cookie_data = {
                'access_code': code,
                'name': access_code.name,
            }
            
            # Serialize the dictionary as JSON and store it in the cookie
            import json
            response.set_cookie('access_data', json.dumps(cookie_data)) 

            return response
        except AccessCode.DoesNotExist:
            messages.error(request, "Invalid or used access code.")
    return render(request, 'enter_access_code.html')

def protected_view(request):
    return render(request, 'protected_view.html')
import requests
from django.http import JsonResponse

def add_judge(request):
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        email_or_phone = request.POST.get('email_or_phone')

        # Generate the AccessCode (JD + 20 random characters)
        access_code = 'JD' + generate_random_code(20)

        # Save the judge to the database (replace 'YourModelName' with your model)
        AccessCode.objects.create(
            name=name,
            code=access_code,
            email_or_phone=email_or_phone
        )

        # Send an SMS using the Termii API
        url = "https://api.ng.termii.com/api/sms/send"
        termii_payload = {
            "to": [email_or_phone],  # Assuming the phone number is provided in email_or_phone
            "from": "CyberSchool",
            "sms": f"Hi there, you have been invited as a judge for the competition. Your access code is: {access_code}. Access the dashboard here: http://127.0.0.1:8000/dashboard/",
            "type": "plain",
            "channel": "generic",
            "api_key": "TLQCTmvmwf5d1MSv3Qxf96e78vrpjVSTmcfA5NvFVulVY8I023Eqvop2OkW8r3",
        }
        termii_headers = {
            'Content-Type': 'application/json',
        }

        # Send the SMS using requests
        termii_response = requests.request("POST", url, headers=termii_headers, json=termii_payload)
        print(termii_response.text)

        # Check if the SMS was sent successfully
        if termii_response.status_code == 200:
            # Return a success message or other data
            return JsonResponse({'message': 'Judge added successfully and SMS sent'})
        else:
            # Handle SMS sending failure
            return JsonResponse({'message': 'Judge added successfully, but SMS sending failed'})

    # Handle other HTTP methods if needed
    return JsonResponse({'message': 'Invalid request method'})


def generate_random_code(length):
    import random
    import string
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

from django.http import JsonResponse
from django.urls import reverse

# Your view code here

def check_submission(request):
    if request.method == 'POST':
        auto_id = request.POST.get('auto_id')

        try:
            submission = Submission.objects.get(auto_id=auto_id)
            # Auto ID exists in the database, return the redirect URL
            return JsonResponse({'redirect_url': reverse('view_submission', args=[auto_id])})
        except Submission.DoesNotExist:
            # Auto ID doesn't exist, return an error message
            return JsonResponse({'error': 'Submission not found'}, status=404)

from django.core.paginator import Paginator

def user_list(request):
    # Retrieve all submissions from the database
    submissions = Submission.objects.all()
    
    # Initialize the query variable
    query = request.GET.get('q')
    
    if query:
        submissions = submissions.filter(
            Q(name__icontains=query) |
            Q(state_of_origin__icontains=query) |
            Q(educational_institution__icontains=query)
        )
    
    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(submissions, per_page=10)
    page = paginator.get_page(page_number)
    
    submissions_count = submissions.count()

    context = {
        'submissions': page,  # Use the paginated page object in the context
        'submissions_count': submissions_count,
        'query': query,  # Pass the query back to the template for displaying in the search input
    }

    return render(request, 'entry_list.html', context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
