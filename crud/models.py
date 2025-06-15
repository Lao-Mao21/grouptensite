from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# Create your models here.

class ManageRoom(models.Model):
    class Meta:
        db_table = 'manageroom_tbl'
    room_id = models.AutoField(primary_key=True, blank=False, null=False)
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe'),
    ]
    room_type = models.CharField(max_length=100, blank=False, null=False, choices=ROOM_TYPE_CHOICES)
    room_number = models.CharField(max_length=50, blank=False, null=False, unique=True)
    bed_count = models.IntegerField(blank=False, null=False)
    BED_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('deluxe', 'Deluxe'),
        ('VIP', 'VIP'),
        ('king', 'King'),
        ('queen', 'Queen'),
        ('bunk', 'Bunk Bed'),
        ('futon', 'Futon'),
    ]
    bed_type = models.CharField(max_length=100, blank=False, null=False , choices=BED_TYPE_CHOICES)
    floor = models.CharField(max_length=50, blank=False, null=False)
    ROOM_STATUS_CHOICES = [
        ('available', 'Available'),
        ('maintenance', 'Maintenance'),
        ('cleaning', 'Cleaning'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ]
    room_status = models.CharField(max_length=30, choices=ROOM_STATUS_CHOICES, default='available', blank=False, null=False)
    room_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    PRICE_TYPE_CHOICES = [
        ('per hour', 'Per Hour'),
        ('per day/night', 'Per Day/Night'),
        ('custom', 'Custom Price'),
    ]
    room_price_type = models.CharField(max_length=100, choices=PRICE_TYPE_CHOICES, blank=False, null=False)
    available_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.get_room_type_display()}"

class AdminAccounts(models.Model):
    class Meta:
        db_table = 'adminaccounts_tbl'
    is_active = models.BooleanField(default=True)
    admin_id = models.AutoField(primary_key=True, blank=False, null=False)
    first_name = models.CharField(max_length=155, blank=False, null=False)
    middle_name = models.CharField(max_length=155, blank=True, null=True)
    last_name = models.CharField(max_length=155, blank=False, null=False)
    full_name = models.CharField(max_length=310, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    date_of_birth = models.DateField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            # Check if password is already in use
            hashed_password = make_password(self.password)
            if AdminAccounts.objects.filter(password=hashed_password).exists() or GuestAccounts.objects.filter(password=hashed_password).exists():
                raise ValueError("This password is already in use. Please choose a different password.")
            self.password = hashed_password
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_username(self):
        """Return the username for this User."""
        return self.username

    def __str__(self):
        return self.full_name

class GuestAccounts(models.Model):
    class Meta:
        db_table = 'guestaccounts_tbl'
    guest_id = models.AutoField(primary_key=True, blank=False, null=False)
    first_name = models.CharField(max_length=155, blank=False, null=False)
    middle_name = models.CharField(max_length=155, blank=True, null=True)
    last_name = models.CharField(max_length=155, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=310, blank=False, null=False)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    date_of_birth = models.DateField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    card_last_four = models.CharField(max_length=4, blank=True, null=True)
    card_type = models.CharField(max_length=20, blank=True, null=True)
    card_expiry = models.CharField(max_length=5, blank=True, null=True)
    card_holder_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            # Check if password is already in use
            hashed_password = make_password(self.password)
            if AdminAccounts.objects.filter(password=hashed_password).exists() or GuestAccounts.objects.filter(password=hashed_password).exists():
                raise ValueError("This password is already in use. Please choose a different password.")
            self.password = hashed_password
        super().save(*args, **kwargs)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_username(self):
        """Return the username for this User."""
        return self.username

    def __str__(self):
        return self.full_name

class ManageGuest(models.Model):
    class Meta:
        db_table = 'manageguest_tbl'
    guest_id = models.ForeignKey(GuestAccounts, on_delete=models.CASCADE, related_name='guests', null=True, blank=True)
    guest_name = models.CharField(max_length=155, blank=False, null=False)
    room_id = models.ForeignKey(ManageRoom, on_delete=models.CASCADE, related_name='guests')
    status = models.CharField(max_length=20, blank=False, null=False)
    check_in = models.DateTimeField(blank=False, null=False)
    check_out = models.DateTimeField(blank=False, null=False)
    expected_arrival = models.DateTimeField(blank=False, null=False)
    guest_count = models.IntegerField(default=1, blank=False, null=False)
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
    ]
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default='cash', blank=False, null=False)
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
        ('no booking','No Booking'),
    ]
    payment_status = models.CharField(max_length=40, choices=PAYMENT_STATUS_CHOICES, default='no booking', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GuestArchive(models.Model):
    class Meta:
        db_table = 'guestarchive_tbl'
    guest_name = models.CharField(max_length=255)
    room_id = models.ForeignKey(ManageRoom, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    guest_count = models.IntegerField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    payment_status = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=50)
    guest_id = models.ForeignKey(GuestAccounts, on_delete=models.CASCADE)

class PaymentTransaction(models.Model):
    class Meta:
        db_table = 'payment_transactions_tbl'
    
    transaction_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(GuestAccounts, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(ManageGuest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ])
    payment_method = models.CharField(max_length=50)
    transaction_reference = models.CharField(max_length=100, unique=True, blank=True, null=True)
    payment_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"