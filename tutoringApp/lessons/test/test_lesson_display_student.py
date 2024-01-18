"""Tests for the `lesson_display_student` page."""
import tempfile
from datetime import datetime, timedelta, timezone

from django.test import override_settings
from django.urls import reverse
from freezegun import freeze_time
from parameterized import parameterized

from lessons.models import Entry, Lesson, Solution, TaskStatusChoices
from utils.testing import TestCaseLessonsUtils

LESSON_DATE = datetime(2023, 12, 12, 8, tzinfo=timezone.utc)


class TestLessonDisplayStudent(TestCaseLessonsUtils):
    """Tests for the functionality of displaying Lesson objects from Student's perspective."""

    def setUp(self):
        """Initial database setup."""
        super().setUp()

        lesson = Lesson.objects.get(pk=1)
        lesson.title = "Lesson's title"
        lesson.subject = "Lesson's subject"
        lesson.subject_details = "Lesson's subject details"
        lesson.save()

    def test_all_lesson_data_displayed_correctly(self):
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-summary-main-title">Lesson's title</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-summary-main-table-cell-bottom main-table-cell-bottom">Dec. 12, 2023, 8 a.m.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-summary-main-table-cell-bottom main-table-cell-bottom">tutor1's first name tutor1's last name</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-summary-main-table-cell-bottom main-table-cell-bottom">student1's first name student1's last name</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-subject-main-top main-table-cell-top">Lesson's subject</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-subject-main-bottom main-table-cell-bottom">Lesson's subject details</div>""",
            html=True,
        )

    def test_edit_btn_not_displayed(self):
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertNotContains(
            res,
            """<div class="edit-btn button_fill_green">
                                        <a href="/lessons/update/1">
                                            Edit
                                        </a>
                                    </div>""",
            html=True,
        )

    def test_subject_displayed_correctly(self):
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-summary-main-table-cell-bottom main-table-cell-bottom">Math</div>""",
            html=True,
        )

    @freeze_time(LESSON_DATE - timedelta(hours=1))
    def test_correct_status_displayed_before_lesson(self):
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom status-entry-bottom_green">Have not taken place</div>""",
            html=True,
        )

        self.assertContains(
            res,
            """<div class="lesson-left-status-main-table-cell-bottom main-table-cell-bottom">Have not taken place</div>""",
            html=True,
        )

    @freeze_time(LESSON_DATE + timedelta(minutes=5))
    def test_correct_status_displayed_during_lesson(self):
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom status-entry-bottom_green">Currently taking place</div>""",
            html=True,
        )

        self.assertContains(
            res,
            """<div class="lesson-left-status-main-table-cell-bottom main-table-cell-bottom">Currently taking place</div>""",
            html=True,
        )

    @freeze_time(LESSON_DATE + timedelta(days=1))
    def test_correct_status_displayed_after_lesson(self):
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom status-entry-bottom_green">Took place already</div>""",
            html=True,
        )

        self.assertContains(
            res,
            """<div class="lesson-left-status-main-table-cell-bottom main-table-cell-bottom">Took place already</div>""",
            html=True,
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_realated_material_in_db_displayed_correctly(self):
        lesson = Lesson.objects.get(pk=1)
        material = self._create_material_object(lesson=lesson, name="Material file")
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            f"""
            <a href="{material.file.url}" download="">
                Material file
            </a>
            """,
            html=True,
        )

    def test_related_task_in_db_displayed_correctly(self):
        lesson = Lesson.objects.get(pk=1)
        self._create_task_object(
            lesson=lesson,
            title="Task 1",
            description="Description of task 1.",
            due_data=LESSON_DATE + timedelta(days=2),
        )
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-header-text-main">Task 1</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-description">Description of task 1.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-due_date">Due Dec. 14, 2023, 8 a.m.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-header-text-status status_red">Solution pending</div>""",
            html=True,
        )

    def test_related_tasks_in_db_no_solution_uploaded_add_btn_displayed(self):
        lesson = Lesson.objects.get(pk=1)
        self._create_task_object(
            lesson=lesson,
            title="Task 1",
            description="Description of task 1.",
            due_data=LESSON_DATE + timedelta(days=2),
        )
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-student_solution-button">
                <label for="lesson-left-tasks-main-task-student_solution-button-input-input-0">
                    <div class="lesson-left-tasks-main-task-student_solution-button-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"></path>
                        </svg>
                    </div>
                </label>
                <div class="lesson-left-tasks-main-task-student_solution-button-input hidden">
                    <input type="file" class="lesson-left-tasks-main-task-student_solution-button-input-input" id="lesson-left-tasks-main-task-student_solution-button-input-input-0" data-index="0" data-task="1">
                </div>
            </div>""",
            html=True,
        )

    def test_related_tasks_in_db_no_solution_uploaded_correst_status_displayed(self):
        lesson = Lesson.objects.get(pk=1)
        self._create_task_object(
            lesson=lesson,
            title="Task 1",
            description="Description of task 1.",
            due_data=LESSON_DATE + timedelta(days=2),
        )
        self._login_user(username="student1", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">1 outstanding.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">None with rejected solution.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_orange">None to be checked.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom status-entry-bottom_green">None finished.</div>""",
            html=True,
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_related_tasks_in_db_solution_uploaded_correctly_displayed(self):
        self._login_user(username="student1", password="haslo123")
        lesson = Lesson.objects.get(pk=1)
        task = self._create_task_object(
            lesson=lesson,
            title="Task 1",
            description="Description of task 1.",
            due_data=LESSON_DATE + timedelta(days=2),
        )
        self._create_solution(task)
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        solution = Solution.objects.get(pk=1)

        self.assertContains(
            res,
            f"""<div class="lesson-left-tasks-main-task-student_solution-file_uploaded">
                                        <div class="lesson-left-tasks-main-task-student_solution-file_uploaded-left">
                                            <div class="lesson-left-tasks-main-task-student_solution-file_uploaded-left-file-icon">
                                                
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-filetype-pdf" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5zM1.6 11.85H0v3.999h.791v-1.342h.803c.287 0 .531-.057.732-.173.203-.117.358-.275.463-.474a1.42 1.42 0 0 0 .161-.677c0-.25-.053-.476-.158-.677a1.176 1.176 0 0 0-.46-.477c-.2-.12-.443-.179-.732-.179Zm.545 1.333a.795.795 0 0 1-.085.38.574.574 0 0 1-.238.241.794.794 0 0 1-.375.082H.788V12.48h.66c.218 0 .389.06.512.181.123.122.185.296.185.522Zm1.217-1.333v3.999h1.46c.401 0 .734-.08.998-.237a1.45 1.45 0 0 0 .595-.689c.13-.3.196-.662.196-1.084 0-.42-.065-.778-.196-1.075a1.426 1.426 0 0 0-.589-.68c-.264-.156-.599-.234-1.005-.234H3.362Zm.791.645h.563c.248 0 .45.05.609.152a.89.89 0 0 1 .354.454c.079.201.118.452.118.753a2.3 2.3 0 0 1-.068.592 1.14 1.14 0 0 1-.196.422.8.8 0 0 1-.334.252 1.298 1.298 0 0 1-.483.082h-.563v-2.707Zm3.743 1.763v1.591h-.79V11.85h2.548v.653H7.896v1.117h1.606v.638H7.896Z"></path>
                    </svg>               
                </div>
                <div class="lesson-left-tasks-main-task-student_solution-file_uploaded-left-file-name link-container">
                    <a href="{solution.solution.url}" download="">
                        {solution.solution.name.split("/")[-1]}
                    </a>
                </div>
            </div>
            <div class="lesson-left-tasks-main-task-student_solution-file_uploaded-right">
                <div class="lesson-left-tasks-main-task-student_solution-file_uploaded-right-delete icon_green" data-pk="1" data-index="0" data-task="1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                    </svg>
                </div>
            </div>
        </div>""",
            html=True,
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_related_tasks_in_db_solution_uploaded_correct_task_status_displayed(self):
        self._login_user(username="student1", password="haslo123")
        lesson = Lesson.objects.get(pk=1)
        task = self._create_task_object(
            lesson=lesson,
            title="Task 1",
            description="Description of task 1.",
            due_data=LESSON_DATE + timedelta(days=2),
        )
        self._create_solution(task)
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-header-text-status status_orange">Solution uploaded</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">None outstanding.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">None with rejected solution.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_orange">1 to be checked.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom status-entry-bottom_green">None finished.</div>""",
            html=True,
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_related_tasks_in_db_solution_uploaded_and_approved_correct_task_status_displayed(
        self,
    ):
        self._login_user(username="student1", password="haslo123")
        lesson = Lesson.objects.get(pk=1)
        task = self._create_task_object(
            lesson=lesson,
            title="Task 1",
            description="Description of task 1.",
            due_data=LESSON_DATE + timedelta(days=2),
        )
        self._create_solution(task)
        task.status = TaskStatusChoices.SOLUTION_APPROVED.value
        task.save()
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-header-text-status status_green">Done</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">None outstanding.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">None with rejected solution.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_orange">None to be checked.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom status-entry-bottom_green">1 finished.</div>""",
            html=True,
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_related_tasks_in_db_solution_uploaded_and_rejectes_correct_task_status_displayed(
        self,
    ):
        self._login_user(username="student1", password="haslo123")
        lesson = Lesson.objects.get(pk=1)
        task = self._create_task_object(
            lesson=lesson,
            title="Task 1",
            description="Description of task 1.",
            due_data=LESSON_DATE + timedelta(days=2),
        )
        self._create_solution(task)
        task.status = TaskStatusChoices.SOLUTION_DISMISSED.value
        task.save()
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1})
        )

        self.assertContains(
            res,
            """<div class="lesson-left-tasks-main-task-header-text-status status_red">Solution dismissed</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">None outstanding.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_red">1 with rejected solution.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom main-table-cell-bottom_orange">None to be checked.</div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-status-main-entry-bottom status-entry-bottom_green">None finished.</div>""",
            html=True,
        )

    def test_correct_entry_form_entry_created(self):
        self._login_user(username="student1", password="haslo123")
        self.client.post(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1}),
            {
                "text": "Entry from Student.",
            },
        )
        self.assertEqual(len(Entry.objects.all()), 1)
        self.assertEqual(Entry.objects.get(pk=1).text, "Entry from Student.")

    @freeze_time(datetime(2023, 12, 13, 10))
    def test_entry_from_student_correctly_displayed(self):
        self._login_user(username="student1", password="haslo123")
        res = self.client.post(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1}),
            {
                "text": "Entry from Student.",
            },
            follow=True,
        )

        self.assertContains(
            res,
            """<div class="lesson-left-tasks-activity-entries-entry-right-top">
                                        student1's first name student1's last name, Dec. 13, 2023, 10 a.m.
                                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="lesson-left-tasks-activity-entries-entry-right-bottom">
                                        Entry from Student.
                                    </div>""",
            html=True,
        )

    @parameterized.expand([False, True])
    def test_user_is_not_related_student_warning_displayed(self, is_student):
        self._register_user("other_user", student=is_student)
        self.client.login(username="other_user", password="haslo123")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1}), follow=True
        )

        self.assertEqual(res.status_code, 403)

    def test_user_is_related_tutor_redirected_to_display_page_for_tutors(self):
        self._login_user("tutor1")
        res = self.client.get(
            reverse("lessons:lesson_display_student", kwargs={"pk": 1}), follow=True
        )

        self.assertRedirects(
            res, reverse("lessons:lesson_display_tutor", kwargs={"pk": 1})
        )
