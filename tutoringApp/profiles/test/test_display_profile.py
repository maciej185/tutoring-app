from django.urls import reverse
from freezegun import freeze_time
from parameterized import parameterized

from utils.testing import TestCaseProfileUtils

NOW = "2023-12-12"


class TestDisplayProfile(TestCaseProfileUtils):
    """Tests for the functionality of displaying user's profile."""

    def test_student_profile_displayed_by_owner_information_correctly_displayed(self):
        username = "student1"
        self.create_profile(username, student=True)
        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(res, f"{username}'s description.", html=True)
        self.assertContains(res, f"{username}'s city.", html=True)
        self.assertContains(res, "Jan. 11, 2000")

        self.assertContains(
            res,
            """<li class="profile-education-main-list-element list-element">
                                        <div class="profile-education-main-list-element-top list-element-top">
                                            School1
                                        </div>
                                        <div class="profile-education-main-list-element-bottom list-element-bottom">
                                            Jan. 11, 2000-Jan. 11, 2003, Additional info about bachelor degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li class="profile-education-main-list-element list-element">
                                        <div class="profile-education-main-list-element-top list-element-top">
                                            School2
                                        </div>
                                        <div class="profile-education-main-list-element-bottom list-element-bottom">
                                            Jan. 12, 2003-Jan. 12, 2005, Additional info about master degree.
                                        </div>
                                    </li>""",
            html=True,
        )

    def test_student_profile_displayed_by_another_student_information_correctly_displayed(
        self,
    ):
        username = "student1"
        self.create_profile(username, student=True)

        self.create_profile("student2", student=True)
        self.client.login(username="student2", password="haslo123")

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(res, f"{username}'s description.", html=True)
        self.assertContains(res, f"{username}'s city.", html=True)
        self.assertContains(res, "Jan. 11, 2000")

        self.assertContains(
            res,
            """<li class="profile-education-main-list-element list-element">
                                        <div class="profile-education-main-list-element-top list-element-top">
                                            School1
                                        </div>
                                        <div class="profile-education-main-list-element-bottom list-element-bottom">
                                            Jan. 11, 2000-Jan. 11, 2003, Additional info about bachelor degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li class="profile-education-main-list-element list-element">
                                        <div class="profile-education-main-list-element-top list-element-top">
                                            School2
                                        </div>
                                        <div class="profile-education-main-list-element-bottom list-element-bottom">
                                            Jan. 12, 2003-Jan. 12, 2005, Additional info about master degree.
                                        </div>
                                    </li>""",
            html=True,
        )

    def test_student_profile_displayed_by_tutor_information_correctly_displayed(self):
        username = "student1"
        self.create_profile(username, student=True)

        self.create_profile("tutor1", student=False)
        self.client.login(username="tutor1", password="haslo123")

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(res, f"{username}'s description.", html=True)
        self.assertContains(res, f"{username}'s city.", html=True)
        self.assertContains(res, "Jan. 11, 2000")

        self.assertContains(
            res,
            """<li class="profile-education-main-list-element list-element">
                                        <div class="profile-education-main-list-element-top list-element-top">
                                            School1
                                        </div>
                                        <div class="profile-education-main-list-element-bottom list-element-bottom">
                                            Jan. 11, 2000-Jan. 11, 2003, Additional info about bachelor degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li class="profile-education-main-list-element list-element">
                                        <div class="profile-education-main-list-element-top list-element-top">
                                            School2
                                        </div>
                                        <div class="profile-education-main-list-element-bottom list-element-bottom">
                                            Jan. 12, 2003-Jan. 12, 2005, Additional info about master degree.
                                        </div>
                                    </li>""",
            html=True,
        )

    def test_tutor_profile_displayed_by_owner_information_correctly_displayed(self):
        username = "tutor1"
        self.create_profile(username, student=False)

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(res, f"{username}'s description.", html=True)
        self.assertContains(res, f"{username}'s city.", html=True)
        self.assertContains(res, "Jan. 11, 2000")

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-education-main-list-school tutor-side-section-main-list-master">
                                            School1
                                        </div>
                                        <div class="tutor-left-education-main-list-details tutor-side-section-main-list-minor">
                                            Jan. 11, 2000-Jan. 11, 2003, Additional info about bachelor degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-education-main-list-school tutor-side-section-main-list-master">
                                            School2
                                        </div>
                                        <div class="tutor-left-education-main-list-details tutor-side-section-main-list-minor">
                                            Jan. 12, 2003-Jan. 12, 2005, Additional info about master degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            Single session - Math
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            100 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            Single session - English
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            120 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            10 sessions - Math
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            800 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-left-profile-main-right-languages-language adjacent-container">
                                        <div class="tutor-left-profile-main-right-languages-language-text">
                                            English
                                        </div>
                                        <div class="tutor-left-profile-main-right-languages-language-level tag">
                                            Beginner
                                        </div>
                                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-left-profile-main-right-languages-language adjacent-container">
                                        <div class="tutor-left-profile-main-right-languages-language-text">
                                            German
                                        </div>
                                        <div class="tutor-left-profile-main-right-languages-language-level tag">
                                            Elementary
                                        </div>
                                    </div>""",
            html=True,
        )

    def test_tutor_profile_displayed_by_another_tutor_information_correctly_displayed(
        self,
    ):
        username = "tutor1"
        self.create_profile(username, student=False)

        self.create_profile("tutor2", student=False)
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(res, f"{username}'s description.", html=True)
        self.assertContains(res, f"{username}'s city.", html=True)
        self.assertContains(res, "Jan. 11, 2000")

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-education-main-list-school tutor-side-section-main-list-master">
                                            School1
                                        </div>
                                        <div class="tutor-left-education-main-list-details tutor-side-section-main-list-minor">
                                            Jan. 11, 2000-Jan. 11, 2003, Additional info about bachelor degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-education-main-list-school tutor-side-section-main-list-master">
                                            School2
                                        </div>
                                        <div class="tutor-left-education-main-list-details tutor-side-section-main-list-minor">
                                            Jan. 12, 2003-Jan. 12, 2005, Additional info about master degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            Single session - Math
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            100 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            Single session - English
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            120 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            10 sessions - Math
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            800 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-left-profile-main-right-languages-language adjacent-container">
                                        <div class="tutor-left-profile-main-right-languages-language-text">
                                            English
                                        </div>
                                        <div class="tutor-left-profile-main-right-languages-language-level tag">
                                            Beginner
                                        </div>
                                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-left-profile-main-right-languages-language adjacent-container">
                                        <div class="tutor-left-profile-main-right-languages-language-text">
                                            German
                                        </div>
                                        <div class="tutor-left-profile-main-right-languages-language-level tag">
                                            Elementary
                                        </div>
                                    </div>""",
            html=True,
        )

    def test_tutor_profile_displayed_by_student_information_correctly_displayed(self):
        username = "tutor1"
        self.create_profile(username, student=False)

        self.create_profile("student1", student=True)
        self.client.login(username="student1", password="haslo123")

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(res, f"{username}'s description.", html=True)
        self.assertContains(res, f"{username}'s city.", html=True)
        self.assertContains(res, "Jan. 11, 2000")

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-education-main-list-school tutor-side-section-main-list-master">
                                            School1
                                        </div>
                                        <div class="tutor-left-education-main-list-details tutor-side-section-main-list-minor">
                                            Jan. 11, 2000-Jan. 11, 2003, Additional info about bachelor degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-education-main-list-school tutor-side-section-main-list-master">
                                            School2
                                        </div>
                                        <div class="tutor-left-education-main-list-details tutor-side-section-main-list-minor">
                                            Jan. 12, 2003-Jan. 12, 2005, Additional info about master degree.
                                        </div>
                                    </li>""",
            html=True,
        )

        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            Single session - Math
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            100 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            Single session - English
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            120 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<li>
                                        <div class="tutor-left-pricing-main-list-service tutor-side-section-main-list-master">
                                            10 sessions - Math
                                        </div>
                                        <div class="tutor-left-pricing-main-list-price tutor-side-section-main-list-minor">
                                            800 $
                                        </div>
                                    </li>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-left-profile-main-right-languages-language adjacent-container">
                                        <div class="tutor-left-profile-main-right-languages-language-text">
                                            English
                                        </div>
                                        <div class="tutor-left-profile-main-right-languages-language-level tag">
                                            Beginner
                                        </div>
                                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-left-profile-main-right-languages-language adjacent-container">
                                        <div class="tutor-left-profile-main-right-languages-language-text">
                                            German
                                        </div>
                                        <div class="tutor-left-profile-main-right-languages-language-level tag">
                                            Elementary
                                        </div>
                                    </div>""",
            html=True,
        )

    def test_student_profile_displayed_by_owner_edit_btns_displayed(self):
        username = "student1"
        self.create_profile(username, student=True)
        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/student/update/1">
                                            Edit
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/password_change">
                                            Change password
                                        </a>
                                    </div>""",
            html=True,
        )

    def test_student_profile_displayed_by_another_student_edit_btns_not_displayed(self):
        username = "student1"
        self.create_profile(username, student=True)

        self.create_profile("student2", student=True)
        self.client.login(username="student2", password="haslo123")

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/student/update/1">
                                            Edit
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/password_change">
                                            Change password
                                        </a>
                                    </div>""",
            html=True,
        )

    def test_student_profile_displayed_by_tutor_edit_btns_not_displayed(self):
        username = "student1"
        self.create_profile(username, student=True)

        self.create_profile("tutor1", student=False)
        self.client.login(username="tutor1", password="haslo123")

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/student/update/1">
                                            Edit
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/password_change">
                                            Change password
                                        </a>
                                    </div>""",
            html=True,
        )

    @freeze_time(NOW)
    def test_tutor_profile_displayed_by_owner_edit_btns_displayed(self):
        username = "tutor1"
        self.create_profile(username, student=False)
        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/tutor/update/1">
                                            Edit
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/password_change">
                                            Change password
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-left-pricing-main-configure centered_button_container">
                        <div class="tutor-left-pricing-main-configure-btn button_white_green">
                            <a href="/tutors/services/1">
                                Configure
                            </a>
                        </div>
                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-right-availability-main-configure centered_button_container">
                        <div class="tutor-right-availability-main-configure-btn button_white_green">
                            <a href="/tutors/availability/1/12/2023">
                                Configure
                            </a>
                        </div>
                    </div>""",
        )

    @freeze_time(NOW)
    def test_tutor_profile_displayed_by_another_tutor_edit_btns_not_displayed(self):
        username = "tutor1"
        self.create_profile(username, student=False)

        self.create_profile("tutor2", student=False)
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/tutor/update/1">
                                            Edit
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/password_change">
                                            Change password
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="tutor-left-pricing-main-configure centered_button_container">
                        <div class="tutor-left-pricing-main-configure-btn button_white_green">
                            <a href="/tutors/services/1">
                                Configure
                            </a>
                        </div>
                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="tutor-right-availability-main-configure centered_button_container">
                        <div class="tutor-right-availability-main-configure-btn button_white_green">
                            <a href="/tutors/availability/1/12/2023">
                                Configure
                            </a>
                        </div>
                    </div>""",
        )

    @freeze_time(NOW)
    def test_tutor_profile_displayed_by_student_edit_btns_not_displayed(self):
        username = "tutor1"
        self.create_profile(username, student=False)

        self.create_profile("student1", student=True)
        self.client.login(username="student1", password="haslo123")

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)

        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/tutor/update/1">
                                            Edit
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="options-btn button_white_green">
                                        <a href="/profiles/password_change">
                                            Change password
                                        </a>
                                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="tutor-left-pricing-main-configure centered_button_container">
                        <div class="tutor-left-pricing-main-configure-btn button_white_green">
                            <a href="/tutors/services/1">
                                Configure
                            </a>
                        </div>
                    </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="tutor-right-availability-main-configure centered_button_container">
                        <div class="tutor-right-availability-main-configure-btn button_white_green">
                            <a href="/tutors/availability/1/12/2023">
                                Configure
                            </a>
                        </div>
                    </div>""",
        )

    def test_student_profile_link_to_display_tutor_owner_correctly_redirected(self):
        username = "student1"
        self.create_profile(username, student=True)

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("profiles:student_display", kwargs={"pk": 1}))

    def test_student_profile_link_to_display_tutor_other_student_correctly_redirected(
        self,
    ):
        username = "student1"
        self.create_profile(username, student=True)

        self.create_profile("student2", student=True)
        self.client.login(username="student2", password="haslo123")

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("profiles:student_display", kwargs={"pk": 1}))

    def test_student_profile_link_to_display_tutor_owner_correctly_redirected(self):
        username = "student1"
        self.create_profile(username, student=True)

        self.create_profile("tutor1", student=False)
        self.client.login(username="tutor1", password="haslo123")

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("profiles:student_display", kwargs={"pk": 1}))

    def test_tutor_profile_link_to_display_student_owner_correctly_redirected(self):
        username = "tutor1"
        self.create_profile(username, student=False)

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("profiles:tutor_display", kwargs={"pk": 1}))

    def test_tutor_profile_link_to_display_student_other_tutor_correctly_redirected(
        self,
    ):
        username = "tutor1"
        self.create_profile(username, student=False)

        self.create_profile("tutor2", student=False)
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("profiles:tutor_display", kwargs={"pk": 1}))

    def test_tutor_profile_link_to_display_student_student_correctly_redirected(self):
        username = "tutor1"
        self.create_profile(username, student=False)

        self.create_profile("student1", student=True)
        self.client.login(username="student1", password="haslo123")

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("profiles:tutor_display", kwargs={"pk": 1}))

    def test_profile_does_not_exist_attempt_to_display_tutors_profile_error_page_displayed(
        self,
    ):
        self._register_user("student1", student=True)

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 2}))

        self.assertEqual(res.status_code, 404)

    def test_profile_does_not_exist_attempt_to_display_student_profile_error_page_displayed(
        self,
    ):
        self._register_user("tutor1", student=False)

        res = self.client.get(reverse("profiles:student_display", kwargs={"pk": 2}))

        self.assertEqual(res.status_code, 404)

    @parameterized.expand(
        [
            (True, True, "profiles/display_student_4_student.html"),
            (True, False, "profiles/display_student_4_tutor.html"),
            (False, True, "profiles/display_tutor_4_student.html"),
            (False, False, "profiles/display_tutor_4_tutor.html"),
        ]
    )
    def test_correct_template_displayed_by_profile_and_viewer_types(
        self,
        profile_owner_is_student: bool,
        displayer_is_student: bool,
        template_name: str,
    ):
        self.create_profile("user1", profile_owner_is_student)
        self.create_profile("user2", displayer_is_student)

        self.client.login(username="user2", password="haslo123")

        res = (
            self.client.get(
                reverse("profiles:student_display", kwargs={"pk": 1}), follow=True
            )
            if profile_owner_is_student
            else self.client.get(
                reverse("profiles:tutor_display", kwargs={"pk": 1}), follow=True
            )
        )

        self.assertIn(template_name, [template.name for template in res.templates])
