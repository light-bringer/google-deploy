import sys
import argparse
from urllib import urlencode
from datetime import datetime, timedelta

from scrapy import cmdline


parser = argparse.ArgumentParser(description='Scraper for booking.com')

# parser.add_argument('--city', help='city for searching', default='Tokyo')
# parser.add_argument('--hotel_name', help='hotel name for searching', default='the-fullterton-singapore')
# parser.add_argument('--start', help='checking in date for searching. format dd/mm/yyyy', default='21/08/2018')
# parser.add_argument('--end', help='checking out date for searching. format dd/mm/yyyy', default='22/08/2018')
# parser.add_argument('--increment', help='interval between scraping day', default=1)
# parser.add_argument('--currency', help='selected currency', default='USD')

parser.add_argument('--city', help='city for searching')
parser.add_argument('--hotel_name', help='hotel name for searching')
parser.add_argument('--start', help='checking in date for searching. format dd/mm/yyyy')
parser.add_argument('--end', help='checking out date for searching. format dd/mm/yyyy')
parser.add_argument('--increment', help='interval between scraping day', default=1)
parser.add_argument('--currency', help='selected currency')

# parser.add_argument('--no_rooms', help='number of rooms for searching')
# parser.add_argument('--no_adults', help='number of Adults for searching')
# parser.add_argument('--no_childrens', help='number of childrens for searching')

args = parser.parse_args()

if ((args.city or args.hotel_name) and args.start and args.end):
    # cmdline.execute(['scrapy', 'crawl', 'booking', '-o', 'booking_hotel.csv', '-a', "city=%s" %args.city, '-a', "hotel=%s" %args.hotel_name, '-a', "checkin=%s" %args.start, '-a', "checkout=%s" %args.end, '-a', "increment=%s" %args.increment, '-a', "currency=%s" %args.currency])

    cmdline.execute(['scrapy', 'crawl', 'booking', '-a', "city=%s" % args.city, '-a',
                     "hotel=%s" % args.hotel_name, '-a', "checkin=%s" % args.start, '-a', "checkout=%s" % args.end,
                     '-a', "increment=%s" % args.increment, '-a', "currency=%s" % args.currency])
else:
    print('Required Field: city(hotel name), checkin, checkout')
    sys.exit(0)

