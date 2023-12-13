"""Endpoints for interacting with models from `Tutors` app."""
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tutors.models import Availability


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
