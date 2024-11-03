from celery import Celery
import os

# Configure Celery to use Redis as the broker
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Default Redis URL
    backend="redis://localhost:6379/1"
)

# Set some Celery configuration if needed
celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)