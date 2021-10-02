from django.test import TestCase
from .models import ComparisonSurvey, Category, User

# Models testing here
class ComparisonSurveyTestSuite(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(username='Test Author', password='pas@nsnn')
        category = Category.objects.create(title='Test')
        ComparisonSurvey.objects.create(topic='Test CSurvey', author=author, description=(random.choice(string.ascii_uppercase + string.digits) for _ in range(500)), rating=3.0, category=category)

    def test_csurvey_description_label(self):
        # Expected: FAIL
        print("Testing first name label display")
        csurvey=ComparisonSurvey.objects.get(id=1)
        field_label = csurvey._meta.get_field('topic').verbose_name
        return self.assertEquals(field_label,'topicc')

    def test_cusrvey_description_max_length(self):
        # Expected: FAIL
        print("Testing csurvey description label display")
        csurvey=ComparisonSurvey.objects.get(id=1)
        max_length = csurvey._meta.get_field('description').max_length
        return self.assertEquals(max_length,800)

# Views testing here
