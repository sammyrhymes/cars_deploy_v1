from django.db import models
import random

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from pillow import *

User = get_user_model()


class MpesaTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=255, null=True)
    checkout_request_id = models.CharField(max_length=255, null=True)
    result_code = models.IntegerField(null=True)
    result_desc = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    mpesa_receipt_number = models.CharField(max_length=255, null=True)
    transaction_date = models.DateTimeField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mpesa_receipt_number}"


class Competition(models.Model):
    car_model = models.CharField(max_length=100)
    car_brand = models.CharField(max_length=100, default='one')
    description = models.TextField()
    specifications = models.TextField()
    image = models.ImageField(upload_to='cars/')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_entries_per_user = models.PositiveIntegerField()
    tickets_sold = models.IntegerField(default=0)

    def total_entries_sold(self):
        return self.entries.count()

    def remaining_entries(self):
        return self.total_tickets - self.total_entries_sold()
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = process_image(self.image)  # Call the image processing function
        super(Competition, self).save(*args, **kwargs)


    def __str__(self):
        return self.car_model
    
class CompetitionImage(models.Model):
    competition = models.ForeignKey(Competition, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return f"Image for {self.competition.car_model}"
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = processimage(self.image)
        super().save(*args, **kwargs)
    

class HolidayCompetition(models.Model):
    name = models.CharField(max_length=100, default='diani')
    description = models.TextField()
    image = models.ImageField(upload_to='cars/')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_entries_per_user = models.PositiveIntegerField()
    tickets_sold = models.IntegerField(default=0)

    def total_entries_sold(self):
        return self.entries.count()

    def remaining_entries(self):
        return self.total_tickets - self.total_entries_sold()
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = process_image(self.image)  # Call the image processing function
        super(HolidayCompetition, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class HoliCompetitionImage(models.Model):
    competition = models.ForeignKey(HolidayCompetition, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return f"Image for {self.competition.name}"
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = processimage(self.image)
        super().save(*args, **kwargs)

    

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name='entries', on_delete=models.CASCADE, null=True, blank=True)
    holiday = models.ForeignKey(HolidayCompetition, related_name='entries', on_delete=models.CASCADE, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only run on creation
            if self.competition:
                # Handle car competition entry
                print(f"Attempting to generate ticket for competition {self.competition.id}")
                try:
                    ticket_number = Ticket.generate_ticket_number(self.competition)
                    print(f"Generated ticket number: {ticket_number}")
                    Ticket.objects.create(user=self.user, competition=self.competition, number=ticket_number)
                    self.competition.tickets_sold += 1
                    self.competition.save()
                except ValueError as e:
                    print(f"Error generating ticket number: {e}")
            elif self.holiday:
                # Handle holiday competition entry
                print(f"Attempting to generate ticket for holiday {self.holiday.id}")
                try:
                    ticket_number = Ticket.generate_ticket_number(self.holiday)
                    print(f"Generated ticket number: {ticket_number}")
                    Ticket.objects.create(user=self.user, holiday=self.holiday, number=ticket_number)
                    self.holiday.tickets_sold += 1
                    self.holiday.save()
                except ValueError as e:
                    print(f"Error generating ticket number: {e}")
        
        super().save(*args, **kwargs)

    def __str__(self):
        if self.competition:
            return f"{self.user.username} - {self.competition.car_model}"
        elif self.holiday:
            return f"{self.user.username} - {self.holiday.name}"
        return f"{self.user.username} - No Competition"
    

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    holiday = models.ForeignKey(HolidayCompetition, on_delete=models.CASCADE, null=True, blank=True)
    number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_ticket_number(competition_or_holiday):
        total_tickets = competition_or_holiday.total_tickets

        # Check if the competition or holiday has sold out
        if competition_or_holiday.tickets_sold >= total_tickets:
            raise ValueError("No more tickets available for this competition/holiday.")

        # Get a list of used ticket numbers for this competition or holiday
        if isinstance(competition_or_holiday, Competition):
            used_numbers = Ticket.objects.filter(competition=competition_or_holiday).values_list('number', flat=True)
        elif isinstance(competition_or_holiday, HolidayCompetition):
            used_numbers = Ticket.objects.filter(holiday=competition_or_holiday).values_list('number', flat=True)

        # Generate the set of available ticket numbers
        available_numbers = set(range(1, total_tickets + 1)) - set(used_numbers)

        # If no numbers are available, raise an error
        if not available_numbers:
            raise ValueError("No available ticket numbers left.")

        # Randomly select a ticket number from the available pool
        return random.choice(list(available_numbers))
    

class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    holiday = models.ForeignKey(HolidayCompetition, on_delete=models.CASCADE, null=True, blank=True)
    win_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='winners/', blank=True, null=True)
    testimonial = models.TextField(blank=True, null=True)

    def __str__(self):
        # Check whether this winner is linked to a car competition or a holiday competition
        if self.competition:
            return f"{self.user.username} - {self.competition.car_model} (Car Competition)"
        elif self.holiday:
            return f"{self.user.username} - {self.holiday.name} (Holiday Competition)"
        else:
            return f"{self.user.username} - Unknown Competition"


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

class BasketItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    holicompetition = models.ForeignKey(HolidayCompetition, on_delete=models.CASCADE, null=True, blank=True)
    ticket_count = models.IntegerField()

    def __str__(self):
        if self.competition:
            return f"{self.ticket_count} tickets for {self.competition.car_model}"
        elif self.holicompetition:
            return f"{self.ticket_count} tickets for {self.holicompetition.name}"
