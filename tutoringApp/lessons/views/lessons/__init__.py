from .display import DisplayLessonStudentView
from .display_api import SolutionAPIView
from .update import UpdateLessonView, delete_material_view, delete_task_view

__all__ = [
    "UpdateLessonView",
    "delete_material_view",
    "delete_task_view",
    "DisplayLessonStudentView",
    "SolutionAPIView",
]
