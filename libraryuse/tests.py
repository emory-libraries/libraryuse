from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
import json
from django.test.simple import DjangoTestSuiteRunner

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

        json_string = ''

        for line in response.streaming_content:
            json_string += line

        data = json.loads(json_string)

        self.assertEquals(data['data'][5][0], 1412136480000)
        self.assertEquals(data['data'][5][1], 3)
        self.assertEquals("%s" % data['meta']['strt_date'], "[u'%s']" % start_date)
        self.assertEquals("%s" % data['meta']['end_date'],"[u'%s']" %  end_date)
        self.assertEquals("%s" % data['meta']['library'], "[u'%s']" % library)
        self.assertEquals("%s" % data['distinct'], "[u'3568']")
        self.assertIsNotNone(data['queried_at'])
