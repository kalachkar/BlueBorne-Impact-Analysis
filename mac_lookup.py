#!/usr/bin/env python

from argparse import ArgumentParser
from os import path
import csv, re, urllib2, json, netaddr, sys


class MacLookup(object):
    def __init__(self, csv_src, csv_dst):
        self.csv_src = csv_src
        self.csv_dst = csv_dst
        self.csv_fields = ["MAC", "Brand", "Prefix"]
        self.vendor_details = {}
        self.r = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        self.get_mac()

    def get_mac(self):
        macs = self.csv_reader()
        for mac, state in macs.items():
            if self.r.match(mac):
                vendor_detail = self.get_vendor_details(mac)
                mac_dialect = vendor_detail[0]
                company = vendor_detail[1]
                mac_prefix = vendor_detail[2]
                try:
                    self.vendor_details[mac_dialect]=(company, mac_prefix,
                                                      state)
                except KeyError as e:
                    print("%s triggered a key error" % (e))
                    sys.exit(1)
            elif mac == self.csv_fields[0]:
                continue
            else:
                print("%s is not a valid MAC" % (mac))
        #self.get_output()
        self.csv_writer()

    def csv_reader(self):
        macs = {}
        for source in self.csv_src:
            try:
                date = path.splitext(path.basename(source))[0]
                self.csv_fields.append(date)
                with open(source, "rb") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        mac = row[0]
                        state = row[1].upper()
                        macs[mac]=[date, state]
            except IOError as e:
                print("Error code %d while reading %s: %s" %
                      (e.errno, source, e.strerror))
                sys.exit(1)
        return(macs)

    def csv_writer(self):
        try:
            with open(self.csv_dst, "wb") as f:
                writer = csv.DictWriter(f, fieldnames=self.csv_fields)
                writer.writeheader()
                for key, value in self.vendor_details.items():
                    writer.writerow({"MAC": key, "Brand": value[0],
                                    "Prefix": value[1],
                                    value[2][0]: value[2][1]})
        except IOError as e:
            print("Error code %d while writing %s: %s" %
                  (e.errno, self.csv_dst, e.strerror))
            sys.exit(1)

    def csv_add(self):
        print 'hoi'
        
    def get_vendor_details(self, mac):
        converted_mac = netaddr.EUI(mac)
        converted_mac.dialect = netaddr.mac_unix
        try:
            oui = converted_mac.oui
        except:
            company, mac_prefix = self.get_vendor_details_online(converted_mac)
            mac_prefix = mac_prefix.replace(":", "-")
            return(str(converted_mac), str(company), str(mac_prefix))
        return(str(converted_mac),
               str(oui.registration().org),
               str(oui.registration().oui))

    def get_vendor_details_online(self, mac):
        opener = urllib2.build_opener()
        opener.addheaders = [("User-Agent", "Mozilla/5.0")]
        response = opener.open("https://macvendors.co/api/%s/json" % (mac))
        vendor_detail = json.loads(response.read())
        if "result" in vendor_detail.keys():
            try:
                company = vendor_detail["result"]["company"]
                mac_prefix = vendor_detail["result"]["mac_prefix"]
                return(company, mac_prefix)
            except KeyError:
                return("N/A", "N/A")
        else:
            print("was not found")

    def get_output(self):
        for key, value in self.vendor_details.items():
            print("Key: %s\nCompany: %s\nPrefix: %s\nDate: %s\nState: %s\n\n" %
                  (key, value[0], value[1], value[2][0], value[2][1]))


def argument_parser():
    parser = ArgumentParser(description="Mac address details -> csv")
    parser.add_argument("-s", "--src", action="append", type=str, required=True,
                        help="Provide source csv")
    parser.add_argument("-d", "--dst", type=str, required=True,
                        help="Provide destination csv")
    args = vars(parser.parse_args())
    return(args)


def main():
    args = argument_parser()
    sources = args["src"]
    destination = args["dst"]
    MacLookup(sources, destination)


if __name__ == "__main__":
    main()
