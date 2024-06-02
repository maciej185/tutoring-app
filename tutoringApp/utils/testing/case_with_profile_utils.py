"""Extenstion of default TestCase with registration of new users."""
from profiles.models import Education, Language, Profile, ProfileLanguageList, School
from tutors.models import Service, Subject

from .case_with_user_utils import TestCaseUserUtils


def create_school_objects() -> None:
    """Create sample instances of the School object.

    The methods populates the temporary database
    with sample, mock instances of the School
    model.
    """
    school1 = School(name="School1", country="Country", city="City")
    school1.save()
    school2 = School(name="School2", country="Country", city="City")
    school2.save()


def create_language_objects() -> None:
    """Create sample instances of the Language object.

    The methods populates the temporary database
    with sample, mock instances of the Language
    model.
    """
    language1 = Language(name="English")
    language1.save()
    language2 = Language(name="German")
    language2.save()


def create_subject_objects() -> None:
    """Create sample instances of the Subject object.

    The methods populates the temporary database
    with sample, mock instances of the Subject
    model.
    """
    subject1 = Subject(name="Math", category=2)
    subject1.save()
    subject2 = Subject(name="English", category=0)
    subject2.save()
    subject3 = Subject(name="Physics", category=1)
    subject3.save()
    subject4 = Subject(name="History", category=3)
    subject4.save()


class TestCaseProfileUtils(TestCaseUserUtils):
    """Extension of TestCaseUserUtils class to add method for creating Profile-related objects.

    The extension allows for registering users, creating Profile
    objects and instances of other related models.
    """

    @classmethod
    def setUpTestData(cls):
        """Populate the database with sample instances of Profile-related models."""
        create_school_objects()
        create_language_objects()
        create_subject_objects()

    def _create_education_objects(self, profile: Profile) -> None:
        """Create instances of the Education model.

            The function populates the temporary database with
            sample, mock instances of the Education model
            so that the functionality of updating these
            objects via page for updating entire profile
            could be tested.

        Args:
                profile: Instance of the Profile model
                        that the newlt created Education
                        object will be linked to.
        """
        education1 = Education(
            profile=profile,
            school=School.objects.get(pk=1),
            start_date="2000-01-11",
            end_date="2003-01-11",
            degree="Bachelor",
            additional_info="Additional info about bachelor degree.",
        )
        education1.save()
        education2 = Education(
            profile=profile,
            school=School.objects.get(pk=2),
            start_date="2003-01-12",
            end_date="2005-01-12",
            degree="Master's",
            additional_info="Additional info about master degree.",
        )
        education2.save()

    def _create_profile_language_list_objects(self, profile: Profile) -> None:
        """Create instances of the ProfileLanguageList model.

            The function populates the temporary database with
            sample, mock instances of the ProfileLanguageList
            model so that the functionality of updating and
            deleting these objects via page for updating entire
            profile could be tested.

        Args:
                profile: Instance of the Profile model
                        that the newly created ProfileLanguageList
                        object will be linked to.
        """
        profile_language_list1 = ProfileLanguageList(
            language=Language.objects.get(pk=1),
            profile=profile,
            level=0,
        )
        profile_language_list1.save()

        profile_language_list2 = ProfileLanguageList(
            language=Language.objects.get(pk=2),
            profile=profile,
            level=1,
        )
        profile_language_list2.save()

    def _create_service_objects(self, profile: Profile) -> None:
        """Create instances of the Service model.

            The function populates the temporary database with
            sample, mock instances of the Service
            model so that the functionality of updating and
            deleting these objects via page for updating entire
            profile could be tested.

        Args:
                profile: Instance of the Profile model
                        that the newly created Service
                        object will be linked to.
        """
        service1 = Service(
            tutor=profile,
            subject=Subject.objects.get(pk=1),
            number_of_hours=1,
            price_per_hour=100,
            session_length=60,
            is_default=True,
        )
        service1.save()

        service2 = Service(
            tutor=profile,
            subject=Subject.objects.get(pk=2),
            number_of_hours=1,
            price_per_hour=120,
            session_length=60,
            is_default=True,
        )
        service2.save()

        service3 = Service(
            tutor=profile,
            subject=Subject.objects.get(pk=1),
            number_of_hours=10,
            price_per_hour=80,
            session_length=60,
            is_default=False,
        )
        service3.save()

        service4 = Service(
            tutor=profile,
            subject=Subject.objects.get(pk=2),
            number_of_hours=10,
            price_per_hour=100,
            session_length=60,
            is_default=False,
        )
        service4.save()

    def create_profile(self, username: str, student: bool) -> None:
        """Register user and create instances of Profile-related models.

        The method registers a new user which at the same time
        creates a corresponding instance of the Profile object.
        Depending on the type of profile created, additional
        objects related to that profile are instantiated (Education,
        ProfileLanguageList and Service)

        Args:
            username: Username for the User object that will be created.
            student: Boolean flag indicating whether the profile should be
                    created for a student.
        """
        self._register_user(username=username, student=student)

        profile = Profile.objects.get(user__username=username)

        profile.description = f"{username}'s description."
        profile.city = f"{username}'s city."
        profile.date_of_birth = "2000-01-11"

        profile.save()

        self._create_education_objects(profile=profile)

        if not student:
            self._create_profile_language_list_objects(profile=profile)
            self._create_service_objects(profile=profile)
            profile.teaching_since = "2000-01-12"
