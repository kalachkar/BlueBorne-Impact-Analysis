#!/usr/bin/env python

from netaddr import EUI, mac_unix
from sys import argv, exit
import csv, re


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
                        if mac in self.vendor_details.keys():
                            vendor_detail = self.get_vendor_details(mac)
                            mac = vendor_detail[0]
                            mac_info = vendor_detail[1:]
                            vendor_details[mac].append(mac_info)
                        else:
                            vendor_detail = self.get_vendor_details(mac)
                            mac = vendor_detail[0]
                            mac_info = vendor_detail[1:]
                            self.vendor_details[mac]=mac_info
                    else:
                        print("%s is not a MAC" % (mac))
                        continue
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
        except Exception as e:
            return(e)
        return(str(converted_mac), oui.registration().org, oui.registration().oui)

    def get_vendor_details_online(self, mac):
        # https://macvendors.co/api/C0:EE:FB:04:6B:91/json
        print 'hoi'

    def get_output(self):
        for key, value in self.vendor_details.items():
            print("%s: %s" % (key, value))


def main():
    MacLookup('/home/k.dejong/Downloads/scan_results_10-2-2017.csv')


if __name__ == '__main__':
    main()
