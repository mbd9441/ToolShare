from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from tools.models import*
import datetime
from tools.views import register_controller
#####################################################################
#Tests for object creation in models.py
#(1) community
class CommunityTestCase(TestCase):
    def setUp(self):
        Community.objects.create(zip_code="99999")

    def test_community_exists(self):
        community = Community.objects.get(zip_code=99999)
        self.assertEqual(community.zip_code, 99999)

#(2) user
class UserTestCase(TestCase):
    def setUp(self):
        user=User.objects.create_user(username="John",first_name="John",last_name="Smith", password="password")
        UserProfile.objects.create(user=user, community=Community.objects.create(zip_code="99999"))
    
    def test_user_exists(self):
        user = User.objects.get(username="John")
        userP = UserProfile.objects.get(user = user)
        self.assertEqual(userP.user.last_name, "Smith")

#(3) tool
class ToolTestCase(TestCase):
    def setUp(self):
        usertemp=User.objects.create_user(username="John",first_name="John",last_name="Smith", password="password")
        commtemp=Community.objects.create(zip_code="99999")
        ownertemp=UserProfile.objects.create(user=usertemp, community=commtemp)
        tool=Tool.objects.create(tool_name="rake",tool_type=3,tool_desc="For leaf jumping.",rentable=1,owner=ownertemp)
    
    def test_tool_exists(self):
        usertemp = User.objects.get(username="John")
        tool = Tool.objects.filter(tool_name = "rake", owner = User.objects.get(username="John"))[0]
        self.assertEqual(tool.tool_type, 3)

#########################################################################
#Tests for register_controller.py
#(4)all fields filled except user_name
class UserNameFieldTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Email is not a valid email.")

#(5)all fields filled except first_name
class FirstNameFieldTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "First Name is blank.")

#(6)all fields filled except last_name
class LastNameFieldTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Last Name is blank.")

#(7)all fields filled except zip_code
class ZipCodeFieldTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Zip is invalid.")

#(8)all fields filled except passwd
class PasswdFieldTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Passwords do not match.")

#(9)all fields filled except passwd2
class Passwd2FieldTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':''})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Passwords do not match.")

#(10) passwd and passwd2 are not equal
class PasswdEqualityTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'PASS'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Passwords do not match.")

#(11) passwords are both empty
class PasswdBothEmptyTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'', 'passwd2':''})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Password is blank.")

#(12) email isn't in email format
class EmailInvalidTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Email is not a valid email.")

#(13) email is already registered
class EmailAlreadyRegisteredTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'pass'})
        register_controller.register(request)

    def test_user_name_field_not_filled(self):
        request2 = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'matt', 'last_name':'dunn', 'zip_code':'12345', 'passwd':'word', 'passwd2':'word'})
        response = register_controller.register(request2)
        #print response
        self.assertContains(response, "Email already exists!")

#(14) zip code isn't valid(contains letters)
class ZipInvalidLettersTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'ABCDE', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Zip is invalid.")

#(15) zip code isn't valid(incorrect # digits)
class ZipInvalidDigitsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'123', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Zip is invalid.")

#(16) zip code isn't valid(contains punctuation)
class ZipInvalidPunctuationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'12-34', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Zip is invalid.")

#(17) combination of lack of fields
class LackOfFieldsComboTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'', 'zip_code':'12-34', 'passwd':'pass', 'passwd2':'pass2'})
        response = register_controller.register(request)
        #print response
        self.assertContains(response, "Last Name is blank.")
        self.assertContains(response, "Passwords do not match.")

#(18) combination of already registered and invalid zip
class AlreadyRegisteredAndInvalidZipTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'pass'})
        register_controller.register(request)

    def test_user_name_field_not_filled(self):
        request2 = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'matt', 'last_name':'dunn', 'zip_code':'12-34', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request2)
        #print response
        self.assertContains(response, "Email already exists!")
        self.assertContains(response, "Zip is invalid.")

#(19) if no errors; object created
class NoErrorsObjectCreatedTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_name_field_not_filled(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'13492', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        user = User.objects.get(first_name="emily")
        userP = UserProfile.objects.get(user = user)
        list = UserProfile.objects.filter(user=user)
        self.assertTrue(userP in list)

#(20) if errors; no object created
class UserNotCreatedTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_function(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'ABCDE', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        list = User.objects.filter(email="edf7470@g.rit.edu")
        self.assertFalse(list.exists())

#(21) zip_code not already existing; create new community
class CommunityCreatedTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_function(self):
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'12345', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request)
        #print response
        list = Community.objects.filter(zip_code="12345")
        self.assertTrue(list.exists())

#(22) zip_code already exists; no new community created
class CommunityNotCreatedTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.post('/tools/views/register_controller', {'user_name':'edf7470@rit.edu', 'first_name':'emily', 'last_name':'filmer', 'zip_code':'12345', 'passwd':'pass', 'passwd2':'pass'})
        register_controller.register(request)

    def test_function(self):
        
        request2 = self.factory.post('/tools/views/register_controller', {'user_name':'bob7470@rit.edu', 'first_name':'bob', 'last_name':'filmer', 'zip_code':'12345', 'passwd':'pass', 'passwd2':'pass'})
        response = register_controller.register(request2)
        #print response
        list = Community.objects.filter(zip_code="12345")
        answer = list.count()
        self.assertTrue(answer == 1)




































































