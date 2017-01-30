import urllib.request

from scrapy.selector import Selector

URL = "http://www.last.fm/event/4278840+Marissa+Nadler+at+MeetFactory+on+14+December+2016"
page = urllib.request.urlopen(URL)
html_body = page.read()
selector = Selector(text=html_body, type="html")

# get all properties, i.e. elements that have an itemprop attribute:
elements = selector.xpath('.//*[@itemscope]')

# item’s itemtype and the properties’ values
for item in elements:
    item_type = item.xpath('@itemtype').extract()
    print("Type: {}".format(item_type))

    for property in item.xpath('.//*[@itemprop]'):
        property_name = str(property.xpath('@itemprop').extract().pop()).strip().replace('\n','').replace('\t','')
        property_value = str(property.xpath('string(.)').extract().pop()).strip().replace('\n','').replace('\t','')
        line = property.root.sourceline
        print("{}: {}, line: {}".format(property_name, property_value, line))

    print("\n\n")
pass

