"""API endpoints for managinig `Solution` objects."""

from datetime import datetime, timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest, Request
from rest_framework.response import Response
from rest_framework.views import APIView

from lessons.models import (
    Lesson,
    LessonStatusChoices,
    Solution,
    Task,
    TaskStatusChoices,
)
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

            task = Task.objects.get(pk=return_data["task"])
            task.status = TaskStatusChoices.SOLUTION_UPLOADED.value
            task.save()
            return Response(return_data)
        return Response(solution_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk: int) -> Response:
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
        task = Task.objects.get(solution=solution)
        task.status = TaskStatusChoices.SOLUTION_PENDING.value
        task.save()
        solution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskAPIView(APIView):
    """Endpoints for managing `Task` objects."""

    def put(self, request: HttpRequest, pk: int) -> Response:
        """Change Tasks's status.

        The endpoint checks if an object with provided primary key
        exists before attempting to fetch and update it's status.
        If it does not exist, an appropriate message is returned.

        Args:
            request: Instance of the HttpRequest class containing
                    every information about the request sent to the
                    server.
            pk: Primary key of the `Solution` object that is related
                            to a Task which is meant to be updated.
        Returns:
            Instance of the `Response` class with an appropraite
            status code.
        """
        try:
            solution = Solution.objects.get(pk=pk)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task = Task.objects.get(solution=solution)
        task.status = (
            TaskStatusChoices.SOLUTION_DISMISSED.value
            if request.data["status"] == -1
            else TaskStatusChoices.SOLUTION_APPROVED.value
        )
        task.save()
        return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=["PUT"])
def update_lesson_status_view(request: Request, pk: int) -> Response:
    """Update Lesson's status.

    Args:
        request: Instance of the HttpRequest class containing
                every information about the request sent to the
                server.
        pk: Primary key of the Lesson objects that is about to
            be updated.
    Returns:
        Instance of the `Response` class with an appropraite
        status code.
    """
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.data["status"] not in LessonStatusChoices.values:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    lesson.status = request.data["status"]
    lesson.save()
    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=["PUT"])
def update_lesson_absence_view(request: Request, pk: int) -> Response:
    """Update value of Lesson's `absence` field.

    Args:
        request: Instance of the HttpRequest class containing
                every information about the request sent to the
                server.
        pk: Primary key of the Lesson objects that is about to
            be updated.
    Returns:
        Instance of the `Response` class with an appropraite
        status code.
    """
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if lesson.date > datetime.now(tz=timezone.utc):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    lesson.absence = request.data["absence"]
    lesson.save()
    return Response(status=status.HTTP_200_OK)
