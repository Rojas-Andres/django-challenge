from abc import ABC, abstractmethod
import pandas as pd
from customers.serializers import CustomerSerializer, CustomerFileSerializer

from rest_framework.exceptions import ValidationError


class ProcessingStrategy(ABC):
    @abstractmethod
    def processing(self, request) -> None:
        pass


class JsonProcessing(ProcessingStrategy):
    """
    A processing strategy that handles JSON data for customers.

    This strategy processes the request data by deserializing it using the
    `CustomerSerializer` and saving the valid data to the database.

    Attributes:
        None

    Methods:
        processing(request): Processes the request data and returns the serialized data.

    """

    def processing(self, request):
        data = request.data
        serializer = CustomerSerializer(data=data["customers"], many=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        raise ValidationError(serializer.errors)


class TxtProcessing(ProcessingStrategy):
    def processing(self, request):
        """
        Process the customer data from a file.

        Args:
            request (Request): The HTTP request object.

        Returns:
            list: A list of serialized customer data.

        Raises:
            ValidationError: If the serializer is not valid or if there are errors during processing.
        """
        serializer = CustomerFileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            df = pd.read_csv(file, delimiter=',')
            serializer = CustomerSerializer(data=df.to_dict(orient='records'), many=True)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            raise ValidationError(serializer.errors)
        raise ValidationError(serializer.errors)
