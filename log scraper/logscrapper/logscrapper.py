#!/usr/bin/env python
import re
import os
import sys

log_line=r"(?P<ip_address>\S*)\s-\s-\s\[(?P<timestamp>.*?)\]\s{1,2}\"(?P<method>\S*)\s*(?P<request>\S*)\s*(HTTP\/)*(?P<http_version>.*?)\"\s(?P<response_code>\d{3})\s(?P<size>\S*)\s\"-\"\s\"-\""
prod_ssh = r'^/production/file_metadata/modules/ssh/sshd_config\?$'
dev_rep = r'^/dev/report/.*'
prod_ssh_com = re.compile(prod_ssh)
dev_rep_com = re.compile(dev_rep)
log_line_com = re.compile(log_line)

found_prod_ssh = []
total_prod_file_access = 0
total_prod_file_failure = 0

total_failure_codes = 0

total_dev_access = 0
total_dev_objs = {}


class LogScrapper:

    def __init__(self):
        self.found_prod_ssh = []
        self.total_prod_file_access = 0
        self.total_prod_file_failure = 0
        self.total_failure_codes = 0
        self.total_dev_access = 0
        self.total_dev_objs = {}

    def run(self):
        try:
            for line in sys.stdin:
                r = log_line_com.search(line)
                if r:
                    l = r.groupdict()
                    self._production_requests(l)
                    self._failed_requests(l)
                    self._put_requests(l)
        except Exception as e:
            print "Error: An exception happened", e

    def _production_requests(self, l):
        if 'request' in l.keys() and re.match(prod_ssh_com, l['request']):
            self.total_prod_file_access += 1
            if 'response_code' in l.keys() and l['response_code'] != '200':
                self.total_prod_file_failure += 1

    def _failed_requests(self, l):
        if 'response_code' in l.keys() and l['response_code'] != '200':
            self.total_failure_codes += 1

    def _put_requests(self, l):
        if ('method' in l.keys() and l['method'].lower() == "put") and (
                'request' in l.keys() and re.match(dev_rep_com, l['request'])):
            self.total_dev_access += 1
            if 'ip_address' in l.keys():
                if l['ip_address'] in self.total_dev_objs.keys():
                    self.total_dev_objs[l['ip_address']] += 1
                else:
                    self.total_dev_objs[l['ip_address']] = 1

    def print_results(self):
        print "Total production"
        print "total prod access:", self.total_prod_file_access
        print "total prod failure:", self.total_prod_file_failure
        print "============"
        print "Total failures: ", self.total_failure_codes
        print "============"
        print "Total dev"
        print "Total request for dev:", self.total_dev_access
        print "Dev access breakdown by IP:"
        for k, v in self.total_dev_objs.iteritems():
            print "\t%s: %d" % (k, v)


if __name__ == '__main__':

    ls = LogScrapper()
    ls.run()
    ls.print_results()
