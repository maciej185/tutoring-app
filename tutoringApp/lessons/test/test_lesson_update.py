"""Tests for the functionality of updating a single Lesson object."""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from django.core.files import File
from django.test import override_settings
from django.urls import reverse
from freezegun import freeze_time
from parameterized import parameterized

from lessons.models import Lesson, Material, Task
from utils.testing import NOW, TestCaseLessonsUtils


class TestLessonBookingRelatedUpdate(TestCaseLessonsUtils):
    """Tests for the functionality of updating a single Lesson object."""

    def setUp(self):
        """Initial database setup."""
        super().setUp()
        self.client.login(username="tutor1", password="haslo123")

    def test_correct_update_form_lesson_object_updated(self):
        lesson = Lesson.objects.get(pk=1)
        res = self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}),
            data={
                "title": "Lesson's title",
                "subject": "Lesson's subject",
                "subject_details": "Lesson's subject details",
                "date": lesson.date,
                "initial-date": lesson.date,
                "material_set-TOTAL_FORMS": 1,
                "material_set-INITIAL_FORMS": 0,
                "material_set-MIN_NUM_FORMS": 0,
                "task_set-TOTAL_FORMS": 1,
                "task_set-INITIAL_FORMS": 0,
                "task_set-MIN_NUM_FORMS": 0,
            },
            follow=True,
        )

        lesson.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(lesson.title, "Lesson's title")
        self.assertEqual(lesson.subject, "Lesson's subject")
        self.assertEqual(lesson.subject_details, "Lesson's subject details")

    @parameterized.expand(["title", "subject", "subject_details"])
    def test_incorrect_update_form_field_missing_lesson_object_not_updated_message_displayed(
        self, field
    ):
        lesson = Lesson.objects.get(pk=1)
        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": 1,
            "material_set-INITIAL_FORMS": 0,
            "material_set-MIN_NUM_FORMS": 0,
            "task_set-TOTAL_FORMS": 1,
            "task_set-INITIAL_FORMS": 0,
            "task_set-MIN_NUM_FORMS": 0,
        }
        del data[field]
        res = self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        lesson.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "This field is required.")

    def test_date_input_not_visible(self):
        res = self.client.get(reverse("lessons:lesson_update", kwargs={"pk": 1}))
        self.assertContains(
            res, """<div class="lesson-summary-main-date-bottom-input hidden">"""
        )

    @parameterized.expand(range(1, 6))
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_task_objects_in_db_displayed_on_update_page(self, number):
        lesson = Lesson.objects.get(pk=1)

        for i in range(1, number):
            self._create_task_object(
                lesson=lesson,
                title=f"Task's title number {i}",
                description=f"Task's description number {i}",
            )
        res = self.client.get(reverse("lessons:lesson_update", kwargs={"pk": 1}))
        for i in range(1, number):
            self.assertContains(
                res,
                f"""<input type="hidden" name="task_set-{i - 1}-id" value="{i}" id="id_task_set-{i - 1}-id">""",
                html=True,
            )
            self.assertContains(
                res,
                f"""<input type="hidden" name="task_set-{i - 1}-lesson" value="1" id="id_task_set-{i - 1}-lesson">""",
                html=True,
            )

    @parameterized.expand(range(1, 6))
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @freeze_time(NOW)
    def test_correct_task_formset_task_objects_created(self, number):
        lesson = Lesson.objects.get(pk=1)
        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": 1,
            "material_set-INITIAL_FORMS": 0,
            "material_set-MIN_NUM_FORMS": 0,
            "task_set-TOTAL_FORMS": number,
            "task_set-INITIAL_FORMS": 0,
            "task_set-MIN_NUM_FORMS": number - 1,
        }
        for i in range(1, number + 1):
            data.update(
                {
                    f"task_set-{i - 1}-title": f"Task's title number {i}",
                    f"task_set-{i - 1}-due_date": datetime.fromisoformat(NOW)
                    + timedelta(days=i),
                    f"task_set-{i - 1}-description": f"Task's description number {i}",
                }
            )
        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        self.assertEqual(len(Task.objects.all()), number)

    @parameterized.expand(zip([1, 2, 3, 5], [[1], [1, 2], [2, 3], [2, 4, 5]]))
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @freeze_time(NOW)
    def test_task_objects_already_in_db_correct_task_formset_task_objects_updated(
        self, number_of_tasks, tasks_pks_2b_updated
    ):
        lesson = Lesson.objects.get(pk=1)

        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": 1,
            "material_set-INITIAL_FORMS": 0,
            "material_set-MIN_NUM_FORMS": 0,
            "task_set-TOTAL_FORMS": number_of_tasks + 1,
            "task_set-INITIAL_FORMS": number_of_tasks,
            "task_set-MIN_NUM_FORMS": 0,
        }

        for i in range(1, number_of_tasks + 1):
            self._create_task_object(
                lesson=lesson,
                title=f"Task's title number {i}",
                description=f"Task's description number {i}",
            )

        for task_pk in range(1, number_of_tasks + 1):
            task = Task.objects.get(pk=task_pk)
            data.update(
                {
                    f"task_set-{task_pk - 1}-id": task_pk,
                    f"task_set-{task_pk - 1}-lesson": 1,
                    f"task_set-{task_pk - 1}-title": task.title,
                    f"task_set-{task_pk - 1}-due_date": task.due_date,
                    f"task_set-{task_pk - 1}-description": task.description,
                }
            )

        for task_pk in tasks_pks_2b_updated:
            task = Task.objects.get(pk=task_pk)
            data.update(
                {
                    f"task_set-{task_pk - 1}-title": f"{task.title} UPDATED",
                    f"task_set-{task_pk - 1}-due_date": task.due_date,
                    f"task_set-{task_pk - 1}-description": f"{task.description} UPDATED",
                }
            )

        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        for task_pk in tasks_pks_2b_updated:
            task = Task.objects.get(pk=task_pk)
            self.assertIn("UPDATED", task.title)
            self.assertIn("UPDATED", task.description)

    @parameterized.expand(
        zip(
            [1, 2, 3, 5],
            [[1], [1, 2], [2, 3], [2, 4, 5]],
            [
                {"title": True, "due_date": False, "description": True},
                {"title": True, "due_date": True, "description": False},
                {"title": False, "due_date": True, "description": False},
                {"title": True, "due_date": True, "description": True},
            ],
        )
    )
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @freeze_time(NOW)
    def test_task_objects_already_in_db_incorrect_task_formset_data_missing_task_objects_not_updated(
        self, number_of_tasks, tasks_pks_2b_updated, data_missing
    ):
        lesson = Lesson.objects.get(pk=1)

        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": 1,
            "material_set-INITIAL_FORMS": 0,
            "material_set-MIN_NUM_FORMS": 0,
            "task_set-TOTAL_FORMS": number_of_tasks + 1,
            "task_set-INITIAL_FORMS": number_of_tasks,
            "task_set-MIN_NUM_FORMS": 0,
        }

        for i in range(1, number_of_tasks + 1):
            self._create_task_object(
                lesson=lesson,
                title=f"Task's title number {i}",
                description=f"Task's description number {i}",
            )

        for task_pk in range(1, number_of_tasks + 1):
            task = Task.objects.get(pk=task_pk)
            data.update(
                {
                    f"task_set-{task_pk - 1}-id": task_pk,
                    f"task_set-{task_pk - 1}-lesson": 1,
                    f"task_set-{task_pk - 1}-title": task.title,
                    f"task_set-{task_pk - 1}-due_date": task.due_date,
                    f"task_set-{task_pk - 1}-description": task.description,
                }
            )

        for task_pk in tasks_pks_2b_updated:
            task = Task.objects.get(pk=task_pk)
            data.update(
                {
                    f"task_set-{task_pk - 1}-title": ""
                    if data_missing["title"]
                    else f"{task.title} UPDATED",
                    f"task_set-{task_pk - 1}-due_date": ""
                    if data_missing["due_date"]
                    else task.due_date,
                    f"task_set-{task_pk - 1}-description": ""
                    if data_missing["description"]
                    else f"{task.description} UPDATED",
                }
            )

        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        for task_pk in tasks_pks_2b_updated:
            task = Task.objects.get(pk=task_pk)
            if any(data_missing.values()):
                self.assertNotIn("UPDATED", task.title)
                self.assertNotIn("UPDATED", task.description)

    @parameterized.expand(
        zip(
            [1, 2, 3, 5],
            [[1], [1, 2], [2, 3], [2, 4, 5]],
            [1, 3, 2, 1],
        )
    )
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @freeze_time(NOW)
    def test_task_objects_already_in_db_correct_task_formset_task_objects_updated_and_added(
        self, number_of_tasks, tasks_pks_2b_updated, number_of_tasks_2_be_added
    ):
        lesson = Lesson.objects.get(pk=1)

        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": 1,
            "material_set-INITIAL_FORMS": 0,
            "material_set-MIN_NUM_FORMS": 0,
            "task_set-TOTAL_FORMS": number_of_tasks + number_of_tasks_2_be_added + 1,
            "task_set-INITIAL_FORMS": number_of_tasks,
            "task_set-MIN_NUM_FORMS": number_of_tasks_2_be_added,
        }

        for i in range(1, number_of_tasks + 1):
            self._create_task_object(
                lesson=lesson,
                title=f"Task's title number {i}",
                description=f"Task's description number {i}",
            )

        for task_pk in range(1, number_of_tasks + 1):
            task = Task.objects.get(pk=task_pk)
            data.update(
                {
                    f"task_set-{task_pk - 1}-id": task_pk,
                    f"task_set-{task_pk - 1}-lesson": 1,
                    f"task_set-{task_pk - 1}-title": task.title,
                    f"task_set-{task_pk - 1}-due_date": task.due_date,
                    f"task_set-{task_pk - 1}-description": task.description,
                }
            )

        for task_pk in tasks_pks_2b_updated:
            task = Task.objects.get(pk=task_pk)
            data.update(
                {
                    f"task_set-{task_pk - 1}-title": f"{task.title} UPDATED",
                    f"task_set-{task_pk - 1}-due_date": task.due_date,
                    f"task_set-{task_pk - 1}-description": f"{task.description} UPDATED",
                }
            )

        for i in range(1, number_of_tasks_2_be_added + 1):
            data.update(
                {
                    f"task_set-{number_of_tasks + i - 1}-title": f"Task's title number {number_of_tasks + i}",
                    f"task_set-{number_of_tasks + i - 1}-due_date": datetime.fromisoformat(
                        NOW
                    )
                    + timedelta(days=number_of_tasks + i),
                    f"task_set-{number_of_tasks + i - 1}-description": f"Task's description number {number_of_tasks + i}",
                }
            )

        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        for task_pk in tasks_pks_2b_updated:
            task = Task.objects.get(pk=task_pk)
            self.assertIn("UPDATED", task.title)
            self.assertIn("UPDATED", task.description)

        self.assertEqual(
            len(Task.objects.all()), number_of_tasks + number_of_tasks_2_be_added
        )

    @parameterized.expand(range(1, 6))
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_material_objects_in_db_displayed_on_update_page(self, number):
        lesson = Lesson.objects.get(pk=1)

        for i in range(1, number):
            self._create_material_object(lesson=lesson, name=f"Material number {i}")
        res = self.client.get(reverse("lessons:lesson_update", kwargs={"pk": 1}))

        for i in range(1, number):
            self.assertContains(
                res,
                f"""<input type="hidden" name="material_set-{i - 1}-id" value="{i}" id="id_material_set-{i - 1}-id">""",
                html=True,
            )
            self.assertContains(
                res,
                f"""<input type="hidden" name="material_set-{i - 1}-lesson" value="1" id="id_material_set-{i - 1}-lesson">""",
                html=True,
            )

    @parameterized.expand(range(1, 6))
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_correct_material_formset_material_objects_created(self, number):
        lesson = Lesson.objects.get(pk=1)
        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": number,
            "material_set-INITIAL_FORMS": 0,
            "material_set-MIN_NUM_FORMS": number - 1,
            "task_set-TOTAL_FORMS": 1,
            "task_set-INITIAL_FORMS": 0,
            "task_set-MIN_NUM_FORMS": 0,
        }

        files = []

        for i in range(1, number + 1):
            f = open(
                Path(__file__).parent / Path(r"./test_data/material_file.txt"), "rb"
            )
            files.append(f)
            data.update(
                {
                    f"material_set-{i - 1}-file": File(file=f),
                    f"material_set-{i - 1}-name": f"File name number {i}",
                }
            )
        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        [f.close() for f in files]

        self.assertEqual(len(Material.objects.all()), number)

    @parameterized.expand(zip([1, 2, 3, 5], [[1], [1, 2], [2, 3], [2, 4, 5]]))
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_material_object_already_in_db_correct_material_formset_material_formset_updated(
        self, number_of_materials, materials_pks_2b_updated
    ):
        lesson = Lesson.objects.get(pk=1)

        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": number_of_materials + 1,
            "material_set-INITIAL_FORMS": number_of_materials,
            "material_set-MIN_NUM_FORMS": 0,
            "task_set-TOTAL_FORMS": 1,
            "task_set-INITIAL_FORMS": 0,
            "task_set-MIN_NUM_FORMS": 0,
        }

        for i in range(1, number_of_materials + 1):
            self._create_material_object(lesson=lesson, name=f"Material number {i}")

        for material_pk in range(1, number_of_materials + 1):
            material = Material.objects.get(pk=material_pk)
            data.update(
                {
                    f"material_set-{material_pk - 1}-id": material_pk,
                    f"material_set-{material_pk - 1}-lesson": 1,
                    f"material_set-{material_pk - 1}-file": material.file,
                    f"material_set-{material_pk - 1}-name": material.name,
                }
            )

        for material_pk in materials_pks_2b_updated:
            material = Material.objects.get(pk=material_pk)
            data.update(
                {
                    f"material_set-{material_pk - 1}-name": f"{material.name} UPDATED",
                    f"material_set-{material_pk - 1}-file": material.file,
                }
            )

        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        for material_pk in materials_pks_2b_updated:
            material = Material.objects.get(pk=material_pk)
            self.assertIn("UPDATED", material.name)

    @parameterized.expand(
        zip(
            [1, 2, 3, 5],
            [[1], [1, 2], [2, 3], [2, 4, 5]],
            [
                {"name": True, "file": True},
                {"name": True, "file": False},
                {"name": False, "file": True},
                {"name": False, "file": False},
            ],
        )
    )
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_material_object_already_in_db_incorrect_material_formset_material_objects_not_updated(
        self, number_of_materials, materials_pks_2b_updated, data_missing
    ):
        lesson = Lesson.objects.get(pk=1)

        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": number_of_materials + 1,
            "material_set-INITIAL_FORMS": number_of_materials,
            "material_set-MIN_NUM_FORMS": 0,
            "task_set-TOTAL_FORMS": 1,
            "task_set-INITIAL_FORMS": 0,
            "task_set-MIN_NUM_FORMS": 0,
        }

        for i in range(1, number_of_materials + 1):
            self._create_material_object(lesson=lesson, name=f"Material number {i}")

        for material_pk in range(1, number_of_materials + 1):
            material = Material.objects.get(pk=material_pk)
            data.update(
                {
                    f"material_set-{material_pk - 1}-id": material_pk,
                    f"material_set-{material_pk - 1}-lesson": 1,
                    f"material_set-{material_pk - 1}-file": material.file,
                    f"material_set-{material_pk - 1}-name": material.name,
                }
            )

        for material_pk in materials_pks_2b_updated:
            material = Material.objects.get(pk=material_pk)
            data.update(
                {
                    f"material_set-{material_pk - 1}-name": ""
                    if data_missing["name"]
                    else f"{material.name} UPDATED",
                    f"material_set-{material_pk - 1}-file": ""
                    if data_missing["file"]
                    else material.file,
                }
            )

        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        for material_pk in materials_pks_2b_updated:
            material = Material.objects.get(pk=material_pk)
            self.assertNotIn("UPDATED", material.name) if data_missing[
                "name"
            ] else self.assertIn("UPDATED", material.name)

    @parameterized.expand(
        zip(
            [1, 2, 3, 5],
            [[1], [1, 2], [2, 3], [2, 4, 5]],
            [1, 3, 2, 1],
        )
    )
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @freeze_time(NOW)
    def test_material_object_already_in_db_correct_material_formset_material_formset_updated_and_added(
        self,
        number_of_materials,
        materials_pks_2b_updated,
        number_of_materials_2_be_added,
    ):
        lesson = Lesson.objects.get(pk=1)

        data = {
            "title": "Lesson's title",
            "subject": "Lesson's subject",
            "subject_details": "Lesson's subject details",
            "date": lesson.date,
            "initial-date": lesson.date,
            "material_set-TOTAL_FORMS": number_of_materials
            + number_of_materials_2_be_added
            + 1,
            "material_set-INITIAL_FORMS": number_of_materials,
            "material_set-MIN_NUM_FORMS": number_of_materials_2_be_added,
            "task_set-TOTAL_FORMS": 1,
            "task_set-INITIAL_FORMS": 0,
            "task_set-MIN_NUM_FORMS": 0,
        }

        for i in range(1, number_of_materials + 1):
            self._create_material_object(lesson=lesson, name=f"Material number {i}")

        for material_pk in range(1, number_of_materials + 1):
            material = Material.objects.get(pk=material_pk)
            data.update(
                {
                    f"material_set-{material_pk - 1}-id": material_pk,
                    f"material_set-{material_pk - 1}-lesson": 1,
                    f"material_set-{material_pk - 1}-file": material.file,
                    f"material_set-{material_pk - 1}-name": material.name,
                }
            )

        for material_pk in materials_pks_2b_updated:
            material = Material.objects.get(pk=material_pk)
            data.update(
                {
                    f"material_set-{material_pk - 1}-name": f"{material.name} UPDATED",
                    f"material_set-{material_pk - 1}-file": material.file,
                }
            )

        files = []

        for i in range(1, number_of_materials_2_be_added + 1):
            f = tempfile.NamedTemporaryFile(suffix=".pdf")
            f.write(b"Mock file content.")
            f.seek(0)
            files.append(f)
            data.update(
                {
                    f"material_set-{number_of_materials + i - 1}-file": File(file=f),
                    f"material_set-{number_of_materials + i - 1}-name": f"File name number {number_of_materials + i}",
                }
            )

        self.client.post(
            reverse("lessons:lesson_update", kwargs={"pk": 1}), data=data, follow=True
        )

        [f.close() for f in files]

        for material_pk in materials_pks_2b_updated:
            material = Material.objects.get(pk=material_pk)
            self.assertIn("UPDATED", material.name)

    @parameterized.expand(
        [("GET", True), ("GET", False), ("POST", True), ("POST", False)]
    )
    def test_current_user_not_assigned_tutor_redirected_warning_page_displayed(
        self, request_method, is_student
    ):
        self.client.logout()
        self._register_user("user", student=is_student)
        self.client.login(username="user", password="haslo123")

        res = (
            self.client.get(reverse("lessons:lesson_update", kwargs={"pk": 1}))
            if request_method == "GET"
            else self.client.post(reverse("lessons:lesson_update", kwargs={"pk": 1}))
        )

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowed to update Lesson object assigned to the Tutor.",
            status_code=403,
        )
