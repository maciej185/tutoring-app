"""API endpoints for managinig `Solution` objects."""

from rest_framework import status
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from lessons.models import Solution
from lessons.serializers import SolutionSerializer


class SolutionAPIView(APIView):
    """Endpoints for managing `Solution` objects."""

    def post(self, request: HttpRequest) -> Response:
        """Create a `Solution` object based on provided data.

        Args:
            request: Instance of the HttpRequest class containing
                    every information about the request sent to the
                    server, includign that of new `Solution` object
                    that is about to be created.
        Returns:
            Instance of the `Response` class with an appropraite
            status code and or data about newly created `Solution`
            instance.
        """
        solution_serializer = SolutionSerializer(data=request.data)
        if solution_serializer.is_valid():
            solution_instance = solution_serializer.save()
            return_data = solution_serializer.data
            return_data.update({"solution_pk": solution_instance.pk})
            return Response(return_data)
        return Response(solution_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _request: HttpRequest, pk: int) -> Response:
        """Delete a Solution object with the provided PK.

        The endpoint checks if an object with provided primary key
        exists before attempting to fetch and delete it. If it
        does not exist, an appropriate message is returned.

        Args:
            request: Instance of the HttpRequest class containing
                    every information about the request sent to the
                    server.
            pk: Primary key of the `Solution` object that is meant
                to be deleted.
        Returns:
            Instance of the `Response` class with an appropraite
            status code.
        """
        try:
            solution = Solution.objects.get(pk=pk)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        solution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
