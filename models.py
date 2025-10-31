from django.db import models
from django.contrib.auth.models import User

# --- 1. Core User & Access Tables ---

class UserProfile(models.Model):
    USER_ROLES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff/HelpDesk'),
        ('admin', 'Administrator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='patient')

    def __str__(self):
        return f"{self.user.username} - {self.user_role}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_role = models.CharField(max_length=50, default='Help Desk')
    department = models.CharField(max_length=100)

# --- 2. Appointment & Tracking Tables ---

class Room(models.Model):
    ROOM_STATUS = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('cleaning', 'Cleaning Required'),
    )
    room_number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=20, choices=ROOM_STATUS, default='available')
    next_free_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Room {self.room_number} ({self.status})"

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appt_number = models.CharField(max_length=20, unique=True) # Unique Appt ID
    scheduled_time = models.DateTimeField()

# --- 3. Queue & Real-Time Tracking (The core of the system) ---

class QueueTrack(models.Model):
    QUEUE_STEPS = (
        ('checkin', 'Check-in'),
        ('waiting', 'Waiting for Doctor'),
        ('consultation', 'In Consultation'),
        ('lab_pharmacy', 'Lab/Pharmacy'),
        ('billing', 'Billing'),
        ('complete', 'Complete'),
    )
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    token_number = models.CharField(max_length=10, unique=True) # The patient's tracking ID
    current_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    room_allotment = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    queue_status = models.CharField(max_length=20, choices=QUEUE_STEPS, default='checkin')
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Token {self.token_number} - {self.queue_status}"

# --- 4. Operations & Support Tables ---

class Medication(models.Model):
    AVAILABILITY_STATUS = (
        ('yes', 'Yes'),
        ('low', 'Low Stock - Reorder'),
        ('no', 'No'),
    )
    med_name = models.CharField(max_length=100, unique=True)
    stock_level = models.IntegerField(default=0)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='yes')

class Billing(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')