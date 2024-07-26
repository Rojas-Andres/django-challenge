"""
File for models of the app core.
"""
from django.db import models


class BaseModel(models.Model):
    """
    Base model for all models.

    This class provides common fields and methods for all models in the Django project.
    It includes fields such as 'created_at', 'updated_at', 'deleted_at', and 'is_active',
    and methods for saving and updating instances of the model.

    Fields:
    - created_at: A DateTimeField that automatically sets the value to the current date
                    and time when an instance is created.
    - updated_at: A DateTimeField that automatically updates the value to the current date and
                    time when an instance is updated.
    - deleted_at: A DateTimeField that stores the date and time when an instance is deleted.
                    If the instance is not deleted, the value is set to None.

    Methods:
    - save(): Overrides the default save method to set the 'deleted_at' field if the instance is not active.
    - update(): A custom method that calls the save method to update an instance of the model.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        """
        Meta class for BaseModel

        Abstract is True because this model is not a table in the database, is a base for other models.
        """

        abstract = True
