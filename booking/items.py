
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookingItem(scrapy.Item):
    Url = scrapy.Field()
    Property_Name = scrapy.Field()
    Address = scrapy.Field()
    Gps_Coordinates = scrapy.Field()
    Date_Scraped = scrapy.Field()

    Date_Signed_In = scrapy.Field()
    Date_Signed_Out = scrapy.Field()
    Room_Night = scrapy.Field()
    Included_Tax = scrapy.Field()
    Included_Property_Service_Charge = scrapy.Field()
    Inclded_Other_Charges = scrapy.Field()
    Excluded_Tax = scrapy.Field()
    Excluded_Property_Service_Charge = scrapy.Field()
    Excluded_Ohter_Charges = scrapy.Field()

    No_of_Rooms = scrapy.Field()
    Bed_Room_Type = scrapy.Field()
    Bed_Type = scrapy.Field()
    Amenities = scrapy.Field()
    Room_Size = scrapy.Field()
    Sleeps = scrapy.Field()
    Rate = scrapy.Field()
    Maximum_Available_Room = scrapy.Field()
    Included = scrapy.Field()
    Your_Choice = scrapy.Field()
    Cancelation = scrapy.Field()
    Overall_Rating = scrapy.Field()
    Breakfast = scrapy.Field()
    Cleanliness = scrapy.Field()
    Comfort = scrapy.Field()
    Location = scrapy.Field()
    Facilities = scrapy.Field()
    Staff = scrapy.Field()
    Value_For_Money = scrapy.Field()
    Free_Wifi = scrapy.Field()

    Included_Breakfast = scrapy.Field()
    Optional_Breakfast = scrapy.Field()
    Free_Cancelation = scrapy.Field()
    # Cancelation_Fee = scrapy.Field()
    Families = scrapy.Field()
    Couples = scrapy.Field()
    Group_of_Friends = scrapy.Field()
    Solo_Travellers = scrapy.Field()
    Business_Travellers = scrapy.Field()
    Nationality_of_Reviews = scrapy.Field()



