#!/usr/bin/env python

from netaddr import EUI, mac_unix
from sys import argv, exit
import csv, re, urllib2, json


class MacLookup(object):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.vendor_details = {}
        self.r = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        self.get_mac()

    def get_mac(self):
        try:
            with open(self.csv_path, 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    mac = row[0]
                    if self.r.match(mac):
                        #if mac in self.vendor_details.keys():
                        #    vendor_detail = self.get_vendor_details(mac)
                        #    mac_dialect = vendor_detail[0]
                        #    company = vendor_detail[1]
                        #    mac_prefix = vendor_detail[2]
                        #    self.vendor_details[mac].extend([(mac_dialect, company, mac_prefix)])
                        #else:
                        vendor_detail = self.get_vendor_details(mac)
                        mac_dialect = vendor_detail[0]
                        company = vendor_detail[1]
                        mac_prefix = vendor_detail[2]
                        self.vendor_details[mac]=[(mac_dialect, company, mac_prefix)]
                    else:
                        mac = row[0]
                        self.vendor_details[mac]='Invalid MAC'
            f.close()
            self.get_output()
        except IOError as e:
            print("Error %s, %s" % (e.errno, e.strerror))
            exit(1)

    def get_vendor_details(self, mac):
        converted_mac = EUI(mac)
        converted_mac.dialect = mac_unix
        try:
            oui = converted_mac.oui
        except:
            company, mac_prefix = self.get_vendor_details_online(converted_mac)
            mac_prefix = mac_prefix.replace(':', '-')
            return(str(converted_mac), str(company), str(mac_prefix))
        return(str(converted_mac), str(oui.registration().org), str(oui.registration().oui))

    def get_vendor_details_online(self, mac):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        response = opener.open("https://macvendors.co/api/%s/json" % (mac))
        vendor_detail = json.loads(response.read())
        if 'result' in vendor_detail.keys():
            try:
                company = vendor_detail['result']['company']
                mac_prefix = vendor_detail['result']['mac_prefix']
                return(company, mac_prefix)
            except KeyError:
                return('N/A', 'N/A')

    def get_output(self):
        for key, value in self.vendor_details.items():
            print("%s: %s" % (key, value))

    def write_csv(self):
        print('write')


def main():
    MacLookup('/home/k.dejong/Downloads/scan_results_10-2-2017.csv')


if __name__ == '__main__':
    main()
