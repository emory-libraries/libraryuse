from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
import json
import logging
import os

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
        libraries = [
            {
                'library': 'woodruff',
                'date': 1412179500000,
                'count': 5,
                'distinct': 811,
                'total': 845,
                'person_type': 'all'
            },
            {
                'library': 'law',
                'date': 1412179500000,
                'count': 5,
                'distinct': 185,
                'total': 207,
                'person_type': 'student'
            },
            {
                'library': 'health',
                'date': 1412185020000,
                'count': 1,
                'distinct': 10,
                'total': 11,
                'person_type': 'faculty'
            }
        ]

        start_date = '2014-10-01'
        end_date = '2014-10-02'

        for library in libraries:
            response = client.get(reverse('total_usage', kwargs={
                'library': library['library'],
                'person_type': library['person_type'],
                'start': start_date,
                'end': end_date}))

            self.assertEquals(str(response), 'Content-Type: application/json')
            self.assertEquals(response.status_code, 200)

            data = getJsonString(response)

            self.assertEquals(data['data'][5][0], library['date'])
            self.assertEquals(data['data'][5][1], library['count'])
            self.assertEquals("%s" % data['meta']['strt_date'], "[u'%s']" % start_date)
            self.assertEquals("%s" % data['meta']['end_date'], "[u'%s']" % end_date)
            self.assertEquals("%s" % data['meta']['library'], "[u'%s']" % library['library'])
            self.assertEquals("%s" % data['distinct'], "[u'%s']" % library['distinct'])
            self.assertEquals("%s" % data['total'], "[u'%s']" % library['total'])
            self.assertIsNotNone(data['queried_at'])


class DateFormatTestCase(TestCase):
    fixtures = ['test.json']

    def test_json_response(self):
        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': 'all',
            'start': start_date,
            'end': end_date}))

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

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

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

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

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

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

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

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        totalSum = data['total'][0]

        # Student
        client = Client()
        person_type = 'student'

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        studentSum = data['total'][0]

        self.assertTrue(totalSum > studentSum, "Usage filtered by Students should be less than Total Usage")

        # Faculty
        client = Client()
        person_type = 'staff'

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        FacultySum = data['total'][0]

        self.assertTrue(totalSum > FacultySum, "Usage filtered by Faculty should be less than Total Usage")

        # Staff
        client = Client()
        person_type = 'staff'

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        staffSum = data['total'][0]

        self.assertTrue(totalSum > staffSum, "Usage filtered by Staff should be less than Total Usage")


class TotalStudentsByOnOffCampusTestCase(TestCase):
    fixtures = ['test.json']

    def test_json_response(self):
        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'
        person_type = 'student'

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': person_type,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        studentSum = int(data['total'][0])

        client = Client()

        campus = 'Y'

        response = client.get(reverse('on_off_campus', kwargs={
            'library': library,
            'resident': campus,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        onCampusTotal = int(data['total'][0])

        self.assertTrue(studentSum > onCampusTotal,
                        "On campus usage should not be greater than the total student usage.")

        client = Client()

        campus = 'N'

        response = client.get(reverse('on_off_campus', kwargs={
            'library': library,
            'resident': campus,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        offCampusTotal = int(data['total'][0])

        self.assertTrue(studentSum > offCampusTotal,
                        "Off campus usage should not be greater than the total student usage.")

        self.assertTrue(int(studentSum) == (offCampusTotal + onCampusTotal),
                        "Total student usage should add up to the sum of On and Off Campus usage.")


class TotalsByClassificationsTestCase(TestCase):
    fixtures = ['test.json']

    def test_student_classifications(self):
        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': 'all',
            'start': start_date,
            'end': end_date}))

        data = getJsonString(response)

        totalSum = int(data['total'][0])

        classification = 'all'

        client = Client()
        response = client.get(reverse('student_class', kwargs={
            'library': library,
            'classification': classification,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        totalStudents = int(data['total'][0])

        self.assertTrue(totalSum > totalStudents, 'Students filtered usage should not be greater than the total.')

        client = Client()

        classification = "Freshmen"

        response = client.get(reverse('student_class', kwargs={
            'library': library,
            'classification': classification,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        iTotal = int(data['total'][0])

        self.assertTrue(totalStudents > iTotal,
                        'Individual filtered total should not be greater than the total Faculty/Staff usage.')


    def test_faculty_classifications(self):
        client = Client()
        library = 'woodruff'
        start_date = '2014-10-01'
        end_date = '2014-10-02'

        response = client.get(reverse('total_usage', kwargs={
            'library': library,
            'person_type': 'all',
            'start': start_date,
            'end': end_date}))

        data = getJsonString(response)

        totalSum = int(data['total'][0])

        classification = 'all'

        client = Client()
        response = client.get(reverse('faculty_staff_class', kwargs={
            'library': library,
            'classification': classification,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        totalFacultyStaff = int(data['total'][0])

        self.assertTrue(totalSum > totalFacultyStaff,
                        'Faculty/Staff filtered usage should not be greater than the total.')

        client = Client()

        classification = "LITS: Library and IT Services"

        response = client.get(reverse('faculty_staff_class', kwargs={
            'library': library,
            'classification': classification,
            'start': start_date,
            'end': end_date}))

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        data = getJsonString(response)

        Total = int(data['total'][0])

        self.assertTrue(totalFacultyStaff > Total,
                        'Individual filtered total should not be greater than the total Faculty/Staff usage.')

class TopDepartmentTestCase(TestCase):
    fixtures = ['test.json']

    def test_json_response(self):
        client = Client()
        libraries = [
            {
                'library': 'woodruff',
                'label': 'LITS: Library IT Expense',
                'value': 33,
                'distinct': 118,
                'total': 329
            },
            {
                'library': 'law',
                'label': 'School of Law',
                'value': 14,
                'distinct': 7,
                'total': 24
            },
            {
                'library': 'health',
                'label': 'WHSC Library',
                'value': 4,
                'distinct': 39,
                'total': 58
            }
        ]

        title = 'Department'
        start_date = '2014-10-01'
        end_date = '2014-10-02'

        for library in libraries:
            response = client.get(reverse('top_dprtn', kwargs={
                'library': library['library'],
                'start': start_date,
                'end': end_date}))

            self.assertEquals(str(response), 'Content-Type: application/json')
            self.assertEquals(response.status_code, 200)

            data = getJsonString(response)

            self.assertEquals(data['data'][0]['value'], library['value'])
            self.assertEquals(data['data'][0]['label'], library['label'])
            self.assertEquals("%s" % data['meta']['title'], "[u'%s']" % title)
            self.assertEquals("%s" % data['meta']['strt_date'], "[u'%s']" % start_date)
            self.assertEquals("%s" % data['meta']['end_date'], "[u'%s']" % end_date)
            self.assertEquals("%s" % data['meta']['library'], "[u'%s']" % library['library'])
            self.assertEquals("%s" % data['distinct'], "[u'%s']" % library['distinct'])
            self.assertEquals("%s" % data['total'], "[u'%s']" % library['total'])
            self.assertIsNotNone(data['queried_at'])

class TopDivisionTestCase(TestCase):
    fixtures = ['test.json']

    def test_json_response(self):
        client = Client()
        libraries = [
            {
                'library': 'woodruff',
                'label': 'Campus Life Activities',
                'value': 35,
                'distinct': 18,
                'total': 329
            },
            {
                'library': 'law',
                'label': 'LITS: Library and IT Services',
                'value': 2,
                'distinct': 4,
                'total': 24
            },
            {
                'library': 'health',
                'label': 'Emory College',
                'value': 10,
                'distinct': 9,
                'total': 58
            }
        ]

        title = 'Faculty Division'
        start_date = '2014-10-01'
        end_date = '2014-10-02'

        for library in libraries:
            response = client.get(reverse('top_division', kwargs={
                'library': library['library'],
                'start': start_date,
                'end': end_date}))

            self.assertEquals(str(response), 'Content-Type: application/json')
            self.assertEquals(response.status_code, 200)

            data = getJsonString(response)

            self.assertEquals(data['data'][2]['value'], library['value'])
            self.assertEquals(data['data'][2]['label'], library['label'])
            self.assertEquals("%s" % data['meta']['title'], "[u'%s']" % title)
            self.assertEquals("%s" % data['meta']['strt_date'], "[u'%s']" % start_date)
            self.assertEquals("%s" % data['meta']['end_date'], "[u'%s']" % end_date)
            self.assertEquals("%s" % data['meta']['library'], "[u'%s']" % library['library'])
            self.assertEquals("%s" % data['distinct'], "[u'%s']" % library['distinct'])
            self.assertEquals("%s" % data['total'], "[u'%s']" % library['total'])
            self.assertIsNotNone(data['queried_at'])

class TotalAveragesByClassificationTestCase(TestCase):
    fixtures = ['test.json']

    def test_json_response(self):
        client = Client()
        libraries = [
            {
                'library': 'woodruff',
                'value': 17,
                'filter_on': 'stdn_e_clas',
                'class': 'graduate-year-1',
                'label': 'Graduate Year 1'
            },
            {
                'library': 'law',
                'value': 17,
                'filter_on': 'dvsn_n',
                'class': 'school-of-law',
                'label': 'School Of Law'
            },
            {
                'library': 'health',
                'value': 59,
                'filter_on': 'acca_i',
                'class': 'ucol',
                'label': 'UCOL'
            }
        ]

        start_date = '2014-10-01'
        end_date = '2014-10-02'
        start_hour = 12
        end_hour = 14
        dow = 4
        dow_alphe = 'Wednesday'

        for library in libraries:
            response = client.get(reverse('averages', kwargs={
                'library': library['library'],
                'start': start_date,
                'end': end_date,
                'start_hour': start_hour,
                'end_hour': end_hour,
                'dow': dow,
                'filter_on': library['filter_on']}))

            self.assertEquals(str(response), 'Content-Type: application/json')
            self.assertEquals(response.status_code, 200)

            data = getJsonString(response)

            self.assertEquals(int(data['data'][library['class']]['value']), library['value'])
            self.assertEquals("%s" % data['data'][library['class']]['label'], library['label'])
            self.assertEquals("%s" % data['meta']['strt_date'], "[u'%s']" % start_date)
            self.assertEquals("%s" % data['meta']['end_date'], "[u'%s']" % end_date)
            self.assertEquals("%s" % data['meta']['strt_hour'], "[u'%s']" % start_hour)
            self.assertEquals("%s" % data['meta']['end_hour'], "[u'%s']" % end_hour)
            self.assertEquals("%s" % data['meta']['dow'], "[u'%s']" % dow_alphe)

class TotalAveragesTestCase(TestCase):
    fixtures = ['test.json']

    def test_json_response(self):
        client = Client()
        libraries = [
            {
                'library': 'woodruff',
                'average': 845
            },
            {
                'library': 'law',
                'average': 214
            },
            {
                'library': 'health',
                'average': 149
            }
        ]

        start_date = '2014-10-01'
        end_date = '2014-10-02'
        start_hour = 12
        end_hour = 14
        dow = 4

        for library in libraries:
            response = client.get(reverse('total_averages', kwargs={
                'library': library['library'],
                'start': start_date,
                'end': end_date,
                'start_hour': start_hour,
                'end_hour': end_hour,
                'dow': dow}))

            self.assertEquals(str(response), 'Content-Type: application/json')
            self.assertEquals(response.status_code, 200)

            data = getJsonString(response)

            self.assertEquals(int(data['data']['average']), library['average'])
            self.assertEquals(str(data['start_date']), start_date)
            self.assertEquals(str(data['end_date']), end_date)
            self.assertEquals(int(data['start_hour']), start_hour)
            self.assertEquals(int(data['end_hour']), end_hour)
            self.assertEquals(int(data['dow']), dow)


class ClassificationsTestCase(TestCase):
    fixtures = ['test.json']

    def test_json_response(self):
        client = Client()

        response = client.get(reverse('classifications'))

        data = getJsonString(response)

        self.assertEquals(str(response), 'Content-Type: application/json')
        self.assertEquals(response.status_code, 200)

        self.assertEquals(data['student_classes'][5], 'Graduate Year 2')
        self.assertEquals(data['academic_plans'][22], 'Economics & Mathematics')
        self.assertEquals(data['academic_career'][8], 'UBUS')
        self.assertEquals(data['faculty_divisions'][2], 'Graduate School')
        self.assertEquals(data['departments'][32], 'ECAS: Math & Computer Science')