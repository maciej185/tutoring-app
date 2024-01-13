from .display import DisplayLessonStudentView, DisplayLessonTutorView
from .display_api import SolutionAPIView, TaskAPIView
from .update import UpdateLessonView, delete_material_view, delete_task_view

__all__ = [
    "UpdateLessonView",
    "delete_material_view",
    "delete_task_view",
    "DisplayLessonStudentView",
    "DisplayLessonTutorView",
    "SolutionAPIView",
    "TaskAPIView",
]
