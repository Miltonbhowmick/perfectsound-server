from django.db import models


class OrderStatusChoice(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    REJECTED = "rejected", "Rejected"
