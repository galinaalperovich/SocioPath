import time

from selenium import webdriver

from parser.element_feature import ElementFeature
from parser.element_property import ElementProperty
from settings import path_to_phantomjs

tags = ['span', 'time', 'div', 'p', 'h1', 'li', 'h3', 'td', 'h2', 'a',
        'strong', 'h5', 'item', 'dd', 'b', 'tr', 'h4', 'h5', 'dl', 'address',
        'pre', 'font', 'em', 'header', 'var', 'table', 'abbr']

URL_TO_PARSE = "http://www.nymetroparents.com/2015neweventinfo.cfm?id=129066"
driver = webdriver.PhantomJS(executable_path=path_to_phantomjs)

driver.get(URL_TO_PARSE)

# wait until it loads
time.sleep(2)

# find visible elements which have any text
# http://stackoverflow.com/questions/11340038/phantomjs-not-waiting-for-full-page-load :(
elements = driver.find_elements_by_xpath("//*[not(contains(@style,'display:none')) and normalize-space(text())]")

# leave only these tags
elements_property = []
for element in elements:
    try:
        if element.tag_name in tags and element.text != '':
            elements_property.append(ElementProperty(element, URL_TO_PARSE))
    except:
        pass

features = []
for element in elements_property:
    features.append(ElementFeature(element, driver))
