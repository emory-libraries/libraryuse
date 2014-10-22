from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
import json
import logging

logger = logging.getLogger(__name__)


def getJsonString(response):
  json_string = ''

  for line in response.streaming_content:
      json_string += line

  # json.loads will throw an error if json is not valid.
  return json.loads(json_string)

class TotalUsageTestCase(TestCase):

    fixtures = ['test.json']

    def test_json_response(self):

        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': 'all', \
                                        'start': start_date, \
                                        'end': end_date }))



        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        self.assertEquals(data['data'][5][0], 1412179500000)
        self.assertEquals(data['data'][5][1], 5)
        self.assertEquals("%s" % data['meta']['strt_date'], "[u'%s']" % start_date)
        self.assertEquals("%s" % data['meta']['end_date'],"[u'%s']" %  end_date)
        self.assertEquals("%s" % data['meta']['library'], "[u'%s']" % library)
        self.assertEquals("%s" % data['distinct'], "[u'811']")
        self.assertIsNotNone(data['queried_at'])

class DateFormatTestCase(TestCase):

    fixtures = ['test.json']

    def test_json_response(self):

        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': 'all', \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        self.assertFalse(" " in data['meta']['strt_date'][0], "Start datetime should be in YYYY-MM-DD format.")
        self.assertFalse(" " in data['meta']['end_date'][0], "End datetime should be in YYYY-MM-DD format.")


class TotalUsageByLibraryTestCase(TestCase):

    fixtures = ['test.json']

    def test_woodruff_json_response(self):

        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'
        person_type = 'all'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': person_type, \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        self.assertEquals(data['meta']['library'][0], library)


    def test_law_json_response(self):

        client = Client()
        library = 'law'
        start_date = '2014-10-01'
        end_date = '2014-10-02'
        person_type = 'all'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': person_type, \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        self.assertEquals(data['meta']['library'][0], library)

    def test_health_json_response(self):

        client = Client()
        library = 'health'
        start_date = '2014-10-01'
        end_date = '2014-10-02'
        person_type = 'all'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': person_type, \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        self.assertEquals(data['meta']['library'][0], library)


class TotalUsageByPersonTypeTestCase(TestCase):

    fixtures = ['test.json']

    def test_json_totals(self):

        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'
        person_type = 'all'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': person_type, \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        totalSum = data['total'][0]

        #Student
        client = Client()
        person_type = 'student'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': person_type, \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        studentSum = data['total'][0]

        self.assertTrue(totalSum>studentSum, "Usage filtered by Students should be less than Total Usage")

        #Faculty
        client = Client()
        person_type = 'staff'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': person_type, \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        FacultySum = data['total'][0]

        self.assertTrue(totalSum>FacultySum,"Usage filtered by Faculty should be less than Total Usage")

        #Staff
        client = Client()
        person_type = 'staff'

        response = client.get(reverse('total_usage', kwargs={ \
                                        'library': library, \
                                        'person_type': person_type, \
                                        'start': start_date, \
                                        'end': end_date }))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        staffSum = data['total'][0]

        self.assertTrue(totalSum>staffSum,"Usage filtered by Staff should be less than Total Usage")

class TotalStudentsByOnOffCampusTestCase(TestCase):

      fixtures = ['test.json']

      def test_json_response(self):

          client = Client()
          library = 'woodruff'
          start_date = '2014-10-01'
          end_date = '2014-10-02'
          person_type = 'student'

          response = client.get(reverse('total_usage', kwargs={ \
                                          'library': library, \
                                          'person_type': person_type, \
                                          'start': start_date, \
                                          'end': end_date }))

          self.assertEquals(str(response), 'Content-Type: application/json')
          self.assertEquals(response.status_code, 200)

          data = getJsonString(response)

          studentSum = int(data['total'][0])

          client = Client()

          campus = 'Y'

          response = client.get(reverse('on_off_campus', kwargs={ \
                                          'library': library, \
                                          'resident': campus, \
                                          'start': start_date, \
                                          'end': end_date }))

          self.assertEquals(str(response), 'Content-Type: application/json')
          self.assertEquals(response.status_code, 200)

          data = getJsonString(response)

          onCampusTotal = int(data['total'][0])

          self.assertTrue(studentSum>onCampusTotal,"On campus usage should not be greater than the total student usage.")

          client = Client()

          campus = 'N'

          response = client.get(reverse('on_off_campus', kwargs={ \
                                          'library': library, \
                                          'resident': campus, \
                                          'start': start_date, \
                                          'end': end_date }))

          self.assertEquals(str(response), 'Content-Type: application/json')
          self.assertEquals(response.status_code, 200)

          data = getJsonString(response)

          offCampusTotal = int(data['total'][0])

          self.assertTrue(studentSum>offCampusTotal,"Off campus usage should not be greater than the total student usage.")

          self.assertTrue(int(studentSum)==(offCampusTotal+onCampusTotal),"Total student usage should add up to the sum of On and Off Campus usage.")
<<<<<<< HEAD
=======
          
class TotalsByClassificationsTestCase(TestCase):
  
    fixtures = ['test.json']

    def test_student_classifications(self):
      
      client = Client()
      library = 'woodruff'
      start_date = '2014-10-01'
      end_date = '2014-10-02'

      response = client.get(reverse('total_usage', kwargs={ \
                                      'library': library, \
                                      'person_type': 'all', \
                                      'start': start_date, \
                                      'end': end_date }))
      
      data = getJsonString(response)
      
      totalSum = int(data['total'][0])
      
      classification = 'all'
      
      client = Client()
      response = client.get(reverse('student_class', kwargs={ \
                                      'library': library, \
                                      'classification': classification, \
                                      'start': start_date, \
                                      'end': end_date }))
                                      
      self.assertEquals(str(response), 'Content-Type: application/json')
      self.assertEquals(response.status_code, 200)
      
      data = getJsonString(response)
      
      totalStudents = int(data['total'][0])
      
      self.assertTrue(totalSum>totalStudents, 'Students filtered usage should not be greater than the total.')
      
      
      client = Client()
      
      classification = "Freshmen"
      
      response = client.get(reverse('student_class', kwargs={ \
                                      'library': library, \
                                      'classification': classification, \
                                      'start': start_date, \
                                      'end': end_date }))
                                      
      self.assertEquals(str(response), 'Content-Type: application/json')
      self.assertEquals(response.status_code, 200)
      
      data = getJsonString(response)
      
      iTotal = int(data['total'][0])
      
      self.assertTrue(totalStudents>iTotal, 'Individual filtered total should not be greater than the total Faculty/Staff usage.')

    
    def test_faculty_classifications(self):
      
      client = Client()
      library = 'woodruff'
      start_date = '2014-10-01'
      end_date = '2014-10-02'

      response = client.get(reverse('total_usage', kwargs={ \
                                      'library': library, \
                                      'person_type': 'all', \
                                      'start': start_date, \
                                      'end': end_date }))
      
      data = getJsonString(response)
      
      totalSum = int(data['total'][0])
      
      classification = 'all'
      
      client = Client()
      response = client.get(reverse('faculty_staff_class', kwargs={ \
                                      'library': library, \
                                      'classification': classification, \
                                      'start': start_date, \
                                      'end': end_date }))
                                      
      self.assertEquals(str(response), 'Content-Type: application/json')
      self.assertEquals(response.status_code, 200)
      
      data = getJsonString(response)
      
      totalFacultyStaff = int(data['total'][0])
      
      self.assertTrue(totalSum>totalFacultyStaff, 'Faculty/Staff filtered usage should not be greater than the total.')
      
      
      client = Client()
      
      classification = "LITS: Library and IT Services"
      
      response = client.get(reverse('faculty_staff_class', kwargs={ \
                                      'library': library, \
                                      'classification': classification, \
                                      'start': start_date, \
                                      'end': end_date }))
                                      
      self.assertEquals(str(response), 'Content-Type: application/json')
      self.assertEquals(response.status_code, 200)
      
      data = getJsonString(response)
      
      iTotal = int(data['total'][0])
      
      self.assertTrue(totalFacultyStaff>iTotal, 'Individual filtered total should not be greater than the total Faculty/Staff usage.')
>>>>>>> 14aa2f87931507b5459407ce59d8ed3351cd81e4
