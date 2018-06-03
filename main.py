import sys
import argparse
from urllib import urlencode
from datetime import datetime, timedelta

from scrapy import cmdline


parser = argparse.ArgumentParser(description='Scraper for booking.com')

# parser.add_argument('--city', help='city for searching', default='Tokyo')
# parser.add_argument('--start', help='checking in date for searching. format dd/mm/yyyy', default='21/08/2018')
# parser.add_argument('--end', help='checking out date for searching. format dd/mm/yyyy', default='31/08/2018')
# parser.add_argument('--increment', help='interval between scraping day', default=1)

parser.add_argument('--city', help='city for searching')
parser.add_argument('--start', help='checking in date for searching. format dd/mm/yyyy')
parser.add_argument('--end', help='checking out date for searching. format dd/mm/yyyy')
parser.add_argument('--increment', help='interval between scraping day', default=1)

# parser.add_argument('--no_rooms', help='number of rooms for searching')
# parser.add_argument('--no_adults', help='number of Adults for searching')
# parser.add_argument('--no_childrens', help='number of childrens for searching')

args = parser.parse_args()

if (args.city and args.start and args.end):
    cmdline.execute(['scrapy', 'crawl', 'booking', '-o', 'booking_hotel.csv', '-a', "city=%s" %args.city, '-a', "checkin=%s" %args.start, '-a', "checkout=%s" %args.end, '-a', "increment=%s" %args.increment])
else:
    print ('Required Field: city, checkin, checkout')
    sys.exit(0)



