from django.test import TestCase
from edivorce.apps.core.models import UserResponse, Question, BceidUser
from edivorce.apps.core.utils.user_response import is_complete
from edivorce.apps.core.utils.question_step_mapping import question_step_mapping


# Create your tests here.
class UserResponseTestCase(TestCase):
    fixtures = ['Question.json']

    def setUp(self):
        BceidUser.objects.create(user_guid='1234')
        Question.objects.create(key='test', name='this is test')

    def test_which_order(self):
        step = 'which_orders'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required question
        create_response(user, 'want_which_orders', '["nothing"]')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

    def test_your_info(self):
        step = 'your_information'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # Testing required questions
        # Missing few required questions
        create_response(user, 'name_you', 'John Doe')
        create_response(user, 'last_name_before_married_you', 'Jackson')
        create_response(user, 'birthday_you', '11/11/1111')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # Few required questions with one checking question with hidden question not shown
        create_response(user, 'lived_in_bc_you', '11/11/1111')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with one checking question with hidden question not shown
        create_response(user, 'last_name_born_you', 'Jackson')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with one checking question with hidden question missing
        UserResponse.objects.filter(question_id='lived_in_bc_you').update(value="Moved to British Columbia on")

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with one checking question with hidden question
        create_response(user, 'moved_to_bc_date_you', '12/12/1212')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with two checking question with one hidden and one shown
        create_response(user, 'any_other_name_you', 'NO')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

        # All required questions with two checking question with one hidden question missing
        UserResponse.objects.filter(question_id='any_other_name_you').update(value="YES")

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with all checking question with all hidden questions
        create_response(user, 'other_name_you', 'Smith')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

    def test_your_spouse(self):
        step = 'your_spouse'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # Testing required questions
        # Missing few required questions
        create_response(user, 'name_spouse', 'John Doe')
        create_response(user, 'last_name_before_married_spouse', 'Jackson')
        create_response(user, 'birthday_spouse', '11/11/1111')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # Few required questions with one checking question with hidden question not shown
        create_response(user, 'any_other_name_spouse', 'NO')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with one checking question with hidden question not shown
        create_response(user, 'last_name_born_spouse', 'Jackson')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with one checking question with hidden question missing
        UserResponse.objects.filter(question_id='any_other_name_spouse').update(value="YES")

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with one checking question with hidden question
        create_response(user, 'lived_in_bc_spouse', '11/11/1111')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with two checking question with one hidden and one shown
        create_response(user, 'other_name_spouse', 'Smith')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

        # All required questions with two checking question with one hidden question missing
        UserResponse.objects.filter(question_id='lived_in_bc_spouse').update(value="Moved to British Columbia on")

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required questions with all checking question with all hidden questions
        create_response(user, 'moved_to_bc_date_spouse', '12/12/1212')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

    def test_your_marriage(self):
        pass

    def test_your_separation(self):
        step = 'your_separation'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required question
        create_response(user, 'no_reconciliation_possible', 'I agree')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

    def test_spousal_support(self):
        step = 'spousal_support'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # One required question
        create_response(user, 'spouse_support_details', 'I will support you')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # Two required questions
        create_response(user, 'spouse_support_act', 'Family Law')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

        # Remove first added required response to test the second required question
        UserResponse.objects.get(question_id='spouse_support_details').delete()

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

    def test_property_and_debt(self):
        step = 'property_and_debt'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required question with no hidden shown
        create_response(user, 'deal_with_property_debt', 'equal division')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

        # All required question with hidden shown but no response
        UserResponse.objects.filter(question_id='deal_with_property_debt').update(value="unequal division")

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required question with hidden shown and answered
        create_response(user, 'how_to_divide_property_debt', 'Do not divide them')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

    def test_other_orders(self):
        step = 'other_orders'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required question
        create_response(user, 'other_orders_detail', 'I want more orders')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)

    def test_other_questions(self):
        pass

    def test_filing_locations(self):
        step = 'filing_locations'
        questions = question_step_mapping[step]
        user = BceidUser.objects.get(user_guid='1234')

        # No response should be False
        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), False)

        # All required question
        create_response(user, 'court_registry_for_filing', 'Vancouver')

        lst = UserResponse.objects.filter(question_id__in=questions).values('question_id', 'value')
        self.assertEqual(is_complete(step, lst), True)


# Helper functions
def create_response(user, question, value):
    UserResponse.objects.create(bceid_user=user, question=Question.objects.get(key=question), value=value)