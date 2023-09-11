import uuid
from django.db import models

def generate_auto_id():
    return 'PT' + str(uuid.uuid4().hex)[:10].upper()

class Submission(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    age_range = models.CharField(max_length=20)
    
    # Define choices for Nigerian states with full state names
    NIGERIAN_STATES = [
        ('Abia', 'Abia'),
        ('Adamawa', 'Adamawa'),
        ('Akwa Ibom', 'Akwa Ibom'),
        ('Anambra', 'Anambra'),
        ('Bauchi', 'Bauchi'),
        ('Bayelsa', 'Bayelsa'),
        ('Benue', 'Benue'),
        ('Borno', 'Borno'),
        ('Cross River', 'Cross River'),
        ('Delta', 'Delta'),
        ('Ebonyi', 'Ebonyi'),
        ('Edo', 'Edo'),
        ('Ekiti', 'Ekiti'),
        ('Enugu', 'Enugu'),
        ('Gombe', 'Gombe'),
        ('Imo', 'Imo'),
        ('Jigawa', 'Jigawa'),
        ('Kaduna', 'Kaduna'),
        ('Kano', 'Kano'),
        ('Katsina', 'Katsina'),
        ('Kebbi', 'Kebbi'),
        ('Kogi', 'Kogi'),
        ('Kwara', 'Kwara'),
        ('Lagos', 'Lagos'),
        ('Nasarawa', 'Nasarawa'),
        ('Niger', 'Niger'),
        ('Ogun', 'Ogun'),
        ('Ondo', 'Ondo'),
        ('Osun', 'Osun'),
        ('Oyo', 'Oyo'),
        ('Plateau', 'Plateau'),
        ('Rivers', 'Rivers'),
        ('Sokoto', 'Sokoto'),
        ('Taraba', 'Taraba'),
        ('Yobe', 'Yobe'),
        ('Zamfara', 'Zamfara'),
        ('FCT Abuja', 'FCT Abuja')
    ]
    DOCUMENT_TYPES = [
        ('WORD', 'WORD'),
        ('PDF', 'PDF'),

    ]
    state_of_origin = models.CharField(max_length=20, choices=NIGERIAN_STATES)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    
    educational_institution = models.CharField(max_length=255)
    current_level = models.CharField(max_length=50)
    attachment = models.FileField(upload_to='submissions/')
    auto_id = models.CharField(max_length=12, default=generate_auto_id, unique=True, editable=True)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Grading(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    grader = models.CharField(max_length=200)
    grade = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Grade for {self.submission.name}"
    
# models.py
from django.db import models

class AccessCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    used = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email_or_phone = models.CharField(max_length=255)
    def __str__(self):
        return self.code
