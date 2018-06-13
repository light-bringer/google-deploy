import re
import codecs
from urllib import urlencode
from datetime import datetime, timedelta
from collections import Counter

import requests
requests.packages.urllib3.disable_warnings()
import scrapy
from scrapy import Selector

from booking.items import BookingItem

def get_reviews_by_nationality_on_page(url):
    s = requests.Session()
    r = s.get(url, verify=False, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
    response = Selector(text=r.text)
    # with codecs.open('review.html', 'w', 'utf-8') as f:
    #     f.write(r.text)

    review_items = response.xpath("//li[contains(@class, 'review_item')]")
    # print (len(review_items))
    nationality = []
    for review_item in review_items:
        nationality.append(''.join(review_item.xpath(".//span[@class='reviewer_country']//text()").extract()).replace("\n", '').strip())

    return nationality


def get_reviews_by_nationality(url):
    startTime = datetime.now()
    all_nationality = []
    offset = 0
    review_url = "https://www.booking.com/reviewlist.html?pagename=%s;cc1=%s;type=total;score=;dist=1;rows=100;r_lang=en" %(url.split("/")[-1].split(".")[0], url.split("/")[-2])
    while True:
        url = review_url + ";offset=%d" % offset
        # print url
        reviews_nationlaity = get_reviews_by_nationality_on_page(url)
        # print (reviews_nationlaity)
        if len(reviews_nationlaity) < 1:
            break
        all_nationality.extend(reviews_nationlaity)
        offset += 100

    # print datetime.now() - startTime
    if len(all_nationality) > 0:
        return str(Counter(all_nationality)).replace('Counter({', '').replace('})', '')
    else:
        return "N/A"


# print (get_reviews_by_nationality('https://www.booking.com/hotel/jp/apa-hote-asakusa-taharamachi-ekimae.html'))


class BookingSpider(scrapy.Spider):
    name = "booking"
    host = "https://www.booking.com"
    allowed_domains = ["www.booking.com"]

    def __init__(self, city, hotel, checkin, checkout, increment, currency, *args, **kwargs):
        super(BookingSpider, self).__init__(*args, **kwargs)
        self.city = city
        self.hotel = hotel
        self.min_checkin = datetime.strptime(checkin, '%d/%m/%Y')
        self.max_checkout = datetime.strptime(checkout, '%d/%m/%Y')
        self.increment = int(increment)
        self.currency = currency

    def start_requests(self):
        checkin = self.min_checkin
        while (checkin + timedelta(days=self.increment)) <= self.max_checkout:
            checkout = checkin + timedelta(days=self.increment)
            query_data = {
                # 'ss': self.city,
                'checkin_month': checkin.month,
                'checkin_monthday': checkin.day,
                'checkin_year': checkin.year,
                'checkout_month': checkout.month,
                'checkout_monthday': checkout.day,
                'checkout_year': checkout.year,
                # 'no_rooms': args.no_rooms,
                # 'group_adults': args.no_adults,
                # 'group_children': args.no_childrens
            }

            if self.hotel != "None":
                query_data['ss'] = self.hotel
            else:
                query_data['ss'] = self.city

            if self.currency:
                query_data['selected_currency'] = self.currency

            query_data = dict((k,v) for k,v in query_data.iteritems() if v is not None)
            search_url = "https://www.booking.com/searchresults.en-us.html?"
            url = search_url + urlencode(query_data)
            print(url)

            checkin_string = checkin.strftime('%d/%m/%Y')
            checkout_string = checkout.strftime('%d/%m/%Y')

            yield scrapy.Request(url, meta={'checkin': checkin_string, 'checkout': checkout_string})

            checkin = checkout


    def parse(self, response):
        items = response.xpath("//*[@data-hotelid]")
        for item in items:
            url = self.host + item.xpath(".//a[contains(@class, 'hotel_name_link')]/@href").extract()[0].strip().replace("\n", '')
            print ("URL: ", url)
            yield scrapy.Request(url, callback=self.page_parser, meta={'url': url, 'checkin': response.meta.get('checkin'), 'checkout': response.meta.get('checkout')})

            if self.hotel != "None":
                return

        next_page = response.xpath("//a[contains(@class, 'paging-next')]/@href").extract()
        if len(next_page) > 0:
            print ("\n\n --- PAGE URL --- \n\n", self.host+next_page[0])
            yield scrapy.Request(self.host+next_page[0], callback=self.parse, meta={'checkin': response.meta.get('checkin'), 'checkout': response.meta.get('checkout')})

    def page_parser(self, response):
        # with open('source.html', 'w') as f:
        #     f.write(response.body)

        constants = {}
        canoical_url = response.xpath("//link[@rel='canonical']/@href").extract()[0]
        constants['Nationality_of_Reviews'] = get_reviews_by_nationality(canoical_url)
        constants['Url'] = response.meta.get("url")
        constants['Property_Name'] = response.xpath("//*[@id='hp_hotel_name']/text()").extract()[0].strip()
        constants['Address'] = response.xpath("//*[contains(@class, 'hp_address_subtitle')]/text()").extract()[0].strip()

        raw_coodinate = response.xpath("//*[contains(@class, 'map_static_zoom')]/@style").extract()[0].strip()
        try:
            constants['Gps_Coordinates'] = re.search(r"https://api.mapbox.cn/styles/v1/mapbox/streets-zh-v1/static/(.+?,.+?),", raw_coodinate).group(1)
        except:
            constants['Gps_Coordinates'] = re.search(r"center=(.+?)&", raw_coodinate).group(1)

        constants['Date_Scraped'] = datetime.now().strftime("%B %d, %Y")
        constants['Date_Signed_In'] = response.meta.get('checkin')
        constants['Date_Signed_Out'] = response.meta.get('checkout')
        constants['Room_Night'] = (datetime.strptime(constants['Date_Signed_Out'], '%d/%m/%Y') - datetime.strptime(constants['Date_Signed_In'], '%d/%m/%Y')).days

        hotelier_info = ''.join(response.xpath("//*[@class='hotelier-info']//text()").extract())
        try:
            constants['No_of_Rooms'] = re.search(r"(\d+)\srooms", hotelier_info).group(1)
        except:
            constants['No_of_Rooms'] = "N/A"
        try:
            constants['Overall_Rating'] = response.xpath("//span[@class='review-score-badge']/text()").extract()[0].strip()
        except:
            constants['Overall_Rating'] = 0
        try:
            constants['Cleanliness'] = response.xpath("//ul[@id='review_list_score_breakdown']//*[contains(text(), 'Cleanliness')]/following-sibling::p/text()").extract()[0]
        except:
            constants['Cleanliness'] = ''

        try:
            constants['Comfort'] = response.xpath("//ul[@id='review_list_score_breakdown']//*[contains(text(), 'Comfort')]/following-sibling::p/text()").extract()[0]
        except:
            constants['Comfort'] = ''

        try:
            constants['Location'] = response.xpath("//ul[@id='review_list_score_breakdown']//*[contains(text(), 'Location')]/following-sibling::p/text()").extract()[0]
        except:
            constants['Location'] = ''

        try:
            constants['Facilities'] = response.xpath("//ul[@id='review_list_score_breakdown']//*[contains(text(), 'Facilities')]/following-sibling::p/text()").extract()[0]
        except:
            constants['Facilities'] = ''

        try:
            constants['Staff'] = response.xpath("//ul[@id='review_list_score_breakdown']//*[contains(text(), 'Staff')]/following-sibling::p/text()").extract()[0]
        except:
            constants['Staff'] = ''

        try:
            constants['Value_For_Money'] = response.xpath("//ul[@id='review_list_score_breakdown']//*[contains(text(), 'Value for money')]/following-sibling::p/text()").extract()[0]
        except:
            constants['Value_For_Money'] = ''

        try:
            constants['Free_Wifi'] = response.xpath("//ul[@id='review_list_score_breakdown']//*[contains(text(), 'Free WiFi')]/following-sibling::p/text()").extract()[0]
        except:
            constants['Free_Wifi'] = ''

        try:
            constants['Families'] = response.xpath("//option[@data-customer-type='family_with_children']/@data-quantity").extract()[0]
        except:
            constants['Families'] = "N/A"
        try:
            constants['Couples'] = response.xpath("//option[@data-customer-type='couple']/@data-quantity").extract()[0]
        except:
            constants['Couples'] = "N/A"
        try:
            constants['Group_of_Friends'] = response.xpath("//option[@data-customer-type='review_category_group_of_friends']/@data-quantity").extract()[0]
        except:
            constants['Group_of_Friends'] = "N/A"
        try:
            constants['Solo_Travellers'] = response.xpath("//option[@data-customer-type='solo_traveller']/@data-quantity").extract()[0]
        except:
            constants['Solo_Travellers'] = "N/A"
        try:
            constants['Business_Travellers'] = response.xpath("//option[@data-customer-type='business_traveller']/@data-quantity").extract()[0]
        except:
            constants['Business_Travellers'] = "N/A"

        trs = response.xpath("//tr[@data-block-id]")
        if len(trs) > 0:
            included = ''
            included_status = ''
            for tr in trs:
                room_id = tr.xpath(".//a[contains(@class, 'hprt-roomtype-link')]/@data-room-id").extract()
                if len(room_id) > 0:
                    room_id = room_id[0]
                    constants['Bed_Room_Type'] = ''.join(tr.xpath(".//span[contains(@class, 'hprt-roomtype-icon-link ')]/text()").extract()).replace("\n", '').strip()

                    constants['Bed_Type'] = ''.join(tr.xpath(".//li[contains(@class, 'bed-type')]//text()").extract()).replace("\n", '').strip()
                    if constants['Bed_Type'] == '':
                        constants['Bed_Type'] = ''.join(tr.xpath(".//li[contains(@class, 'bed_type')]//text()").extract()).replace("\n", '').strip()

                    room_info = response.xpath("//div[@data-room-id='%s']"%room_id)
                    constants['Amenities'] = self.get_amenities(room_info)
                    try:
                        constants['Room_Size'] = room_info.xpath(".//strong[contains(text(), 'Size')]/following-sibling::text()").extract()[0].strip()
                    except IndexError:
                        constants['Room_Size'] = \
                        ''.join(room_info.xpath(".//*[@data-name-en='roomsize']//text()").extract()).strip()
                    except Exception:
                        constants['Room_Size'] = ''

                item = BookingItem(constants)
                # print ("Room Id: ", room_id)

                try:
                    item['Sleeps'] = re.search(r"\d+", tr.xpath(".//span[@class='invisible_spoken']/text()").extract()[0].strip()).group()
                except:
                    item['Sleeps'] = ''
                try:
                    item['Rate'] = tr.xpath(".//span[contains(@class, 'hprt-price-price-actual')]/text()").extract()[0].strip()
                except:
                    try:
                        item['Rate'] = tr.xpath(".//span[contains(@class, 'hprt-price-price-standard ')]/text()").extract()[0].strip()
                    except:
                        continue
                try:
                    item['Maximum_Available_Room'] = tr.xpath(".//select[@class='hprt-nos-select']/option/text()").extract()[-1].strip().split("\n")[0]
                except:
                    item['Maximum_Available_Room'] = ''
                try:
                    included = tr.xpath(".//span[contains(text(), 'ncluded:')]/following-sibling::text()").extract()[0].strip()
                    included_status = tr.xpath(".//span[contains(text(), 'ncluded:')]/text()").extract()[0]
                    item = self.get_taxes(included_status, included, item)
                    item['Included'] = included
                except:
                    item = self.get_taxes(included_status, included, item)
                    item['Included'] = included
                li_tags = tr.xpath(".//ul[@class='hprt-conditions']/li")
                if len(li_tags) > 0:
                    item['Your_Choice'] = ''.join(li_tags[0].xpath(".//text()").extract()).replace("\n", ' ').strip()
                    try:
                        item['Breakfast'] = Selector(text=li_tags[0].xpath(".//@data-title").extract()[0].strip()).xpath(".//*[@class='review-score-badge']/text()").extract()[0]
                    except:
                        item['Breakfast'] = ''
                else:
                    item['Your_Choice'] = ''


                item['Cancelation'] = ''
                if len(li_tags) > 1:
                    for li in li_tags[1:]:
                        item['Cancelation'] = item['Cancelation'] + ''.join(li.xpath(".//text()").extract()).replace("\n", ' ').strip() + "\n"

                item = self.get_extractColumns(item)

                yield item
        else:
            room_index = 1
            while True:
                # print ("Room Index", room_index)
                trs = response.xpath("//tr[contains(@class, 'room_loop_counter%d\n')]" %room_index)
                if len(trs) > 2:
                    constants['Bed_Room_Type'] = trs[0].xpath(".//*[contains(@class, 'rt_room_type_ico')]/following-sibling::text()").extract()[0]
                    constants['Bed_Type'] = ''.join(trs[0].xpath(".//li[contains(@class, 'bed-type')]//text()").extract()).replace("\n", '').strip()
                    if constants['Bed_Type'] == '':
                        constants['Bed_Type'] = ''.join(trs[0].xpath(".//li[contains(@class, 'bed_type')]//text()").extract()).replace("\n", '').strip()
                    try:
                        constants['Included'] = trs[0].xpath(".//span[contains(text(), 'ncluded')]/following-sibling::text()").extract()[0].strip()
                        constants = self.get_taxes(trs[0].xpath(".//span[contains(text(), 'ncluded')]/text()").extract()[0], constants['Included'], constants)
                        included = True
                    except:
                        included = False
                    try:
                        constants['Room_Size'] = trs[-1].xpath(".//strong[contains(text(), 'Size')]/following-sibling::text()").extract()[0].strip()
                    except Exception as e:
                        constants['Room_Size'] = 'error'

                    constants['Amenities'] = self.get_amenities(trs[-1])
                    for tr in trs[1:-1]:
                        item = BookingItem(constants)
                        item['Sleeps'] = re.search('\d+', "".join(tr.xpath(".//*[contains(@class, 'roomMaxPersons')]//text()").extract())).group()
                        item['Rate'] = tr.xpath(".//*[contains(@class, 'rooms-table-room-price')]/text()").extract()[0].strip()
                        item['Maximum_Available_Room'] = tr.xpath(".//select[contains(@class, 'room_selectbox')]/option/text()").extract()[-1].strip().split("\n")[0]
                        if not included:
                            try:
                                item['Included'] = tr.xpath(".//span[contains(text(), 'ncluded')]/../following-sibling::text()").extract()[0].strip()
                                item = self.get_taxes(tr.xpath(".//span[contains(text(), 'ncluded')]/text()").extract()[0], item['Included'], item)
                            except:
                                item['Included'] = 'N/A'
                                item['Included_Tax'] = "N/A"
                                item['Included_Property_Service_Charge'] = "N/A"
                                item['Inclded_Other_Charges'] = "N/A"
                                item['Excluded_Tax'] = "N/A"
                                item['Excluded_Property_Service_Charge'] = "N/A"
                                item['Excluded_Ohter_Charges'] = "N/A"

                        li_tags = tr.xpath(".//ul[@class='hp-rt__policy-list']/li")
                        if len(li_tags) > 0:
                            item['Your_Choice'] = ''.join(li_tags[0].xpath(".//text()").extract()).replace("\n", ' ').strip()
                            try:
                                item['Breakfast'] = Selector(text=li_tags[0].xpath(".//@data-title").extract()[0].strip()).xpath(".//*[@class='review-score-badge']/text()").extract()[0]
                            except:
                                item['Breakfast'] = ''
                        else:
                            item['Your_Choice'] = ''
                        item['Cancelation'] = ''
                        if len(li_tags) > 1:
                            for li in li_tags[1:]:
                                item['Cancelation'] = item['Cancelation'] + ''.join(li.xpath(".//text()").extract()).replace("\n", ' ').strip() + "\n"

                        item = self.get_extractColumns(item)

                        yield item

                    room_index += 1
                else:
                    break

    def get_extractColumns(self, item):
        if 'included' in item['Your_Choice']:
            item['Included_Breakfast'] = "Yes"
        else:
            item['Included_Breakfast'] = "No"

        if 'optional' in item['Your_Choice']:
            item['Optional_Breakfast'] = item['Your_Choice'].replace("(optional)", '').replace('Breakfast', '').strip()
        else:
            item['Optional_Breakfast'] = "N/A"

        if 'FREE cancellation' in item['Cancelation']:
            item['Free_Cancelation'] = "Yes"
        else:
            item['Free_Cancelation'] = "No"

        return item

    def get_taxes(self, tax_status, tax_sentence, data):
        if not 'Not included' in tax_status:
            try:
                data['Included_Tax'] = re.search(r"(\d+ %) VAT", tax_sentence).group(1)
            except:
                data['Included_Tax'] = "N/A"
            try:
                data['Included_Property_Service_Charge'] = re.search(r"(\d+ %) Property service charge", tax_sentence).group(1)
            except:
                data['Included_Property_Service_Charge'] = "N/A"
            data['Inclded_Other_Charges'] = [i for i in tax_sentence.split(",") if 'VAT' not in i and 'Property service charge' not in i]
            data['Excluded_Tax'] = "N/A"
            data['Excluded_Property_Service_Charge'] = "N/A"
            data['Excluded_Ohter_Charges'] = "N/A"
        else:
            try:
                data['Excluded_Tax'] = re.search(r"(\d+ %) VAT", tax_sentence).group(1)
            except:
                data['Excluded_Tax'] = "N/A"
            try:
                data['Excluded_Property_Service_Charge'] = re.search(r"(\d+ %) Property service charge", tax_sentence).group(1)
            except:
                data['Excluded_Property_Service_Charge'] = "N/A"
            data['Excluded_Ohter_Charges'] = [i for i in tax_sentence.split(",") if 'VAT' not in i and 'Property service charge' not in i]
            data['Included_Tax'] = "N/A"
            data['Included_Property_Service_Charge'] = "N/A"
            data['Inclded_Other_Charges'] = "N/A"

        return data

    def get_amenities(self, tag):
        amenities= '\n'.join(tag.xpath(".//ul[contains(@class, 'hp_rt_lightbox_facilities')]//li//text()").extract()).replace(u"\u2022", '')
        if amenities == '':
            amenities = '\n'.join(tag.xpath(".//strong[contains(text(), 'Facilities:')]/following-sibling::span/text()").extract()).strip()
        if amenities == '':
            amenities = '\n'.join(tag.xpath(".//strong[contains(text(), 'Facilities:')]/following-sibling::text()").extract()).strip()

        return amenities

