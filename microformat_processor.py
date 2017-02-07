import csv
import urllib.request

from scrapy.selector import Selector

from feature_extractor import FeatureExtractor
from utils import MicroProperty

URL = "http://www.last.fm/event/4278840+Marissa+Nadler+at+MeetFactory+on+14+December+2016"


# get all properties, i.e. elements that have an itemprop attribute:


# item’s itemtype and the properties’ values


def get_scope(type):
    """

    :type type: str
    """
    splits = type.split('/')
    return splits.pop()


def get_properties(url: str) -> dict:
    props = {}
    page = urllib.request.urlopen(url)
    html_body = page.read()
    selector = Selector(text=html_body, type="html")
    elements = selector.xpath('.//*[@itemscope]')
    for item in elements:
        item_type = item.xpath('@itemtype').extract()
        if item_type:
            type = item_type.pop()
        else:
            continue

        props[type] = []
        print("Type: {}".format(item_type))

        items = item.xpath("""set:difference(.//*[@itemprop], .//*[@itemscope]//*[@itemprop])""")
        for prop in items:
            property_name = str(prop.xpath('@itemprop').extract().pop()).strip().replace('\n', '').replace('\t', '')
            property_value = str(prop.xpath('string(.)').extract().pop()).strip().replace('\n', '').replace('\t', '')
            scope = get_scope(type)
            micro_prop = MicroProperty(property_name, property_value, prop, url, type)

            props[type].append(micro_prop)
            # print("{}: {}, line: {}".format(property_name, property_value, line))

        print("\n\n")
    return props


properties = get_properties(URL)
event_properties = []

for k, v in properties.items():
    if 'event' in k.lower():
        event_properties.append(v)

event = event_properties.pop()

file = open('data.csv', 'w')
writer = csv.writer(file)
for prop in event:
    fe = FeatureExtractor(prop)
    row = []  # add all fields
    writer.writerow([])
