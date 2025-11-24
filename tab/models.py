from django.db import models
import uuid
from django.utils import timezone


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    reset_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def set_password(self, raw_password):
        self.password = raw_password  # Replace with make_password(raw_password) for production

    def check_password(self, raw_password):
        return self.password == raw_password  # Replace with check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Session {self.session_id}"


class ChatLog(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='logs')
    user_message = models.TextField()
    bot_response = models.TextField()
    intent = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ChatLog #{self.id} - {self.intent}"


class TaxCalculation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='tax_calculations')
    taxpayer_type = models.CharField(max_length=100)
    regime = models.CharField(max_length=100)
    gross_income = models.FloatField()
    age = models.IntegerField()
    tds = models.FloatField()
    deductions = models.JSONField()
    total_tax = models.FloatField()
    taxable_income = models.FloatField()
    result = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"TaxCalculation #{self.id} for {self.user.username}"


class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=100)
    email = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:50]


class EmailService(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='emails')
    email_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email_type} - {self.user.username}"
