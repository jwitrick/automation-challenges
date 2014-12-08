
import unittest
import sys

from mock import patch, MagicMock
from logscrapper.logscrapper import LogScrapper

data_valid = [
    {'timestamp': '20/Nov/2013:18:18:47 +0000', 'response_code': '200',
        'request': '/production/file_metadata/modules/nscd/nscd.conf?',
        'http_version': '1.1', 'ip_address': '10.39.111.203',
        'method': 'GET', 'size': '298'},
    {'timestamp': '20/Nov/2013:18:18:47 +0000', 'response_code': '500',
        'request': '/production/file_metadata/modules/nscd/nscd.conf?',
        'http_version': '1.1', 'ip_address': '10.39.111.203',
        'method': 'GET', 'size': '298'},
    {'timestamp': '20/Nov/2013:18:18:47 +0000', 'response_code': '200',
        'request': '/production/file_metadata/modules/nscd/nscd.conf?',
        'http_version': '1.1', 'ip_address': '10.39.111.203',
        'method': 'GET', 'size': '298'},
    {'timestamp': '05/Nov/2013:19:53:56 +0000', 'response_code': '200',
        'request': '/production/file_metadata/modules/ssh/sshd_config?',
        'http_version': '1.1', 'ip_address': '10.39.111.201',
        'method': 'GET', 'size': '299'},
    {'timestamp': '05/Nov/2013:19:53:56 +0000', 'response_code': '404',
        'request': '/production/file_metadata/modules/ssh/sshd_config?',
        'http_version': '1.1', 'ip_address': '10.39.111.204',
        'method': 'GET', 'size': '299'},
    {'timestamp': '05/Nov/2013:19:53:56 +0000', 'response_code': '200',
        'request': '/production/file_metadata/modules/ssh/sshd_config?',
        'http_version': '1.1', 'ip_address': '10.39.111.201',
        'method': 'GET', 'size': '299'},
    {'timestamp': '05/Nov/2013:19:53:56 +0000', 'response_code': '300',
        'request': '/test/production/file_metadata/modules/ssh/sshd_config?',
        'http_version': '1.1', 'ip_address': '10.39.111.201',
        'method': 'GET', 'size': '299'}
]

put_data = [
    {'timestamp': '25/Nov/2013:14:27:25 +0000', 'response_code': '200',
        'request': '/dev/report/ec2-184-72-162-170.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.80.174.42',
        'method': 'PUT', 'size': '33'},
    {'timestamp': '25/Nov/2013:15:02:19 +0000', 'response_code': '200',
        'request': '/dev/report/ec2-54-242-115-17.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.80.58.67',
        'method': 'PUT', 'size': '33'},
    {'timestamp': '25/Nov/2013:15:42:30 +0000', 'response_code': '200',
        'request': '/dev/report/ec2-54-205-33-80.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.80.146.96',
        'method': 'PUT', 'size': '33'},
    {'timestamp': '25/Nov/2013:16:19:31 +0000', 'response_code': '200',
        'request': '/dev/report/ec2-54-234-172-116.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.204.211.99',
        'method': 'PUT', 'size': '33'},
    {'timestamp': '25/Nov/2013:16:19:31 +0000', 'response_code': '200',
        'request': '/dev/report/ec2-54-234-172-116.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.204.211.99',
        'method': 'PUT', 'size': '33'},
    {'timestamp': '25/Nov/2013:16:19:31 +0000', 'response_code': '200',
        'request': '/dev/report/ec2-54-234-172-116.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.204.211.99',
        'method': 'GET', 'size': '33'},
    {'timestamp': '25/Nov/2013:16:49:04 +0000', 'response_code': '200',
        'request': '/dev/report/ec2-184-73-47-150.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.204.150.156',
        'method': 'PUT', 'size': '33'},
    {'timestamp': '25/Nov/2013:16:19:31 +0000', 'response_code': '200',
        'request': '/fake/dev/report/ec2-234-172-116.compute-1.amazonaws.com',
        'http_version': '1.1', 'ip_address': '10.204.211.99',
        'method': 'PUT', 'size': '33'}
]

raw_data = [
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "PUT /dev/report/facter/rubypath.rb HTTP/1.1" 200 174 "-" "-"',
   '10.101.3.203 - - [25/Nov/2013:16:51:16 +0000] "PUT /fake/dev/report/validate_slength.rb HTTP/1.1" 200 2594 "-" "-"',
   '10.101.3.204 - - [25/Nov/2013:16:51:16 +0000] "PUT /dev/report/ider/remotefile/cloud.rb HTTP/1.1" 400 4545 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "PUT /dev/report/pe_version.rb HTTP/1.1" 400 1172 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "GET /dev/file_content/obblerrepo/repo.rb HTTP/1.1" 400 3269 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "GET /production/file_metadata/modules/ssh/sshd_config? HTTP/1.1" 200 899 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "GET /production/file_metadata/modules/ssh/sshd_config? HTTP/1.1" 200 444 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "GET /production/file_metadata/modules/ssh/sshd_config? HTTP/1.1" 200 444 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "GET /fake/production/file_metadata/modules/ssh/sshd_config? HTTP/1.1" 200 444 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "GET /production/file_metadata/modules/ssh/sshd_config? HTTP/1.1" 300 444 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "GET /production/file_metadata/modules/ssh/sshd_config? HTTP/1.1" 400 444 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "PUT /dev/file_content/plugins/puppet/parser/functions/strip.rb HTTP/1.1" 200 832 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:16 +0000] "PUT /dev/file_content/plugins/puppet/parser/functions/upcase.rb HTTP/1.1" 200 857 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:17 +0000] "PUT /dev/file_content/plugins/puppet/type/file_line.rb HTTP/1.1" 200 2459 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:17 +0000] "GET /dev/file_content/plugins/puppet/parser/functions/time.rb HTTP/1.1" 200 1059 "-" "-"',
   '10.101.3.205 - - [25/Nov/2013:16:51:17 +0000] "GET /dev/file_content/plugins/puppet/provider/cobblerprofile/profile.rb HTTP/1.1" 400 3321 "-" "-"'
]


class TestLogScrapper(unittest.TestCase):

    def test_production_requests_3_total_one_failed(self):
        lc = LogScrapper()
        for line in data_valid:
            lc._production_requests(line)
        self.assertEqual(3, lc.total_prod_file_access)
        self.assertEqual(1, lc.total_prod_file_failure)

    def test_failed_requests(self):
        lc = LogScrapper()
        for line in data_valid:
            lc._failed_requests(line)
        self.assertEqual(3, lc.total_failure_codes)

    def test_put_requests(self):
        lc = LogScrapper()
        for line in put_data:
            lc._put_requests(line)
        self.assertEqual(6, lc.total_dev_access)
        self.assertEqual(5, len(lc.total_dev_objs.keys()))
        self.assertEqual(1, lc.total_dev_objs['10.80.174.42'])
        self.assertEqual(1, lc.total_dev_objs['10.80.58.67'])
        self.assertEqual(1, lc.total_dev_objs['10.80.146.96'])
        self.assertEqual(2, lc.total_dev_objs['10.204.211.99'])
        self.assertEqual(1, lc.total_dev_objs['10.204.150.156'])

    @patch.object(sys, "stdin")
    def test_run_valid_data(self, mock_stdin):
        mock_stdin.__iter__.return_value = raw_data
        lc = LogScrapper()
        lc.run()
        self.assertEqual(5, lc.total_prod_file_access)
        self.assertEqual(2, lc.total_prod_file_failure)
        self.assertEqual(6, lc.total_failure_codes)
        self.assertEqual(3, lc.total_dev_access)
        self.assertEqual(2, len(lc.total_dev_objs.keys()))
        self.assertEqual(2, lc.total_dev_objs['10.101.3.205'])
        self.assertEqual(1, lc.total_dev_objs['10.101.3.204'])
