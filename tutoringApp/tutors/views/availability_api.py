"""Endpoints for interacting with models from `Tutors` app."""
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tutors.models import Availability
from tutors.serializers import AvailabilitySerializer


class AvailabilityAPIView(APIView):
    """API for interacting with models from `Tutors` app."""

    def delete(self, _request: HttpRequest, pk: int) -> Response:
        """Delete the Availability object with a provided PK.

        The view checks if an object with provided primary key
        exists before attempting to fetch and delete it. If it
        does not exist, an appropriate message is returned.

        Args:
            request: Instance of the HttpRequest class containing
                    every information about the request sent to the
                    server.
            pk: Primary key of the `Availability` object that is meant
                to be deleted.
        Returns:
            Instance of the `Response` class with an appropraite
            status code.
        """
        try:
            availability = Availability.objects.get(pk=pk)
        except Availability.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        availability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: HttpRequest) -> Response:
        """Create new instance of the `Availability` model.

        The new instance of the model is created based on the
        data sent in the request.

        Args:
            request: Instance of the HttpRequest class containing
                    every information about the request sent to the
                    server, includign that of new `Availability` object
                    that is about to be created.
        Returns:
            Instance of the `Response` class with an appropraite
            status code and or data about newly created `Availability`
            instance.
        """
        availability_serializer = AvailabilitySerializer(data=request.data)
        if availability_serializer.is_valid():
            availability_serializer.save()
            return Response(availability_serializer.data)
        return Response(
            availability_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request: HttpRequest) -> Response:
        """Updates existing instance of the `Availability` model.

        The instance is updated based on the data sent in the
        request.

        Args:
            request: Instance of the HttpRequest class containing
                    every information about the request sent to the
                    server, includign that of which `Availability`
                    object should be updated and in what way.
        Returns:
            Instance of the `Response` class with an appropraite
            status code and or data about newly updated `Availability`
            object.
        """
        availability_serializer = AvailabilitySerializer(data=request.data)
        if availability_serializer.is_valid():
            availability_serializer.save()
            return Response(availability_serializer.data)
        return Response(
            availability_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
