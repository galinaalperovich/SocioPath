import time
import urllib.request

from scrapy.selector import Selector

from parser.event_feature import EventFeature
from parser.header import css_header
from parser.micro_property import MicroProperty


def get_microformat_properties(url: str) -> dict:
    try:
        page = urllib.request.urlopen(url)
        if page.code == 200:
            props = {}
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

                items = item.xpath("""set:difference(.//*[@itemprop], .//*[@itemscope]//*[@itemprop])""")
                for prop in items:
                    property_name = str(prop.xpath('@itemprop').extract().pop()).strip().replace('\n', '').replace('\t',
                                                                                                                   '')
                    property_value = str(prop.xpath('string(.)').extract().pop()).strip().replace('\n', '').replace(
                        '\t', '')
                    micro_prop = MicroProperty(property_name, property_value, prop, url, type)

                    props[type].append(micro_prop)
            return props
        return None
    except Exception as e:
        print('{}   {}  {}'.format(now(), 'Problem with microformats for URL:', url))
        return None


def get_microformat_properties_by_type(url, type, queue, i):
    print('{}   Process={}  Getting micro properties for {}'.format(now(), i, url))
    type_properties = []
    micro_properties = get_microformat_properties(url)

    if micro_properties is not None:

        for k, v in micro_properties.items():
            if type in k:
                type_properties.append(v)

    if type_properties:
        queue.put(type_properties)
    else:
        queue.put(None)


def get_event_features(properties, driver, i):
    print("{}   Process={}  {}".format(now(), i, "Extracting features"))
    event = properties.pop()  # TODO might be the list of events!
    event_features = []
    for property in event:
        if property.name in ['startDate', 'endName', 'name', 'description', 'location']:
            try:
                event_feature = EventFeature(property, driver)
            except Exception as e:
                print('{}   Error wih feature extraction {}'.format(now(), e))
                continue

            event_features.append(event_feature)

    return event_features if event_features else None


def write_features(event_features, writer, i, output_file):
    print("{}   Process={}  {}".format(now(), i, "Writing features"))
    for event_feature in event_features:
        if event_feature.webelement is not None:
            row_1_part = [event_feature.url, event_feature.meta_name, event_feature.text_property,
                          event_feature.xy_coords['x'], event_feature.xy_coords['y'],
                          event_feature.block_size['height'], event_feature.block_size['width'],
                          event_feature.tag,
                          event_feature.num_childs, event_feature.num_siblings
                          ]
            css_prop = event_feature.css_prop
            row_2_part = [css_prop.get(css_h, None) for css_h in css_header]
            # row_2_part = [x for x in event_feature.css_prop.values()]
            writer.writerow(row_1_part + row_2_part)
            output_file.flush()


def get_event_features_and_write(properties, driver, writer, i, output_file):
    event_features = None

    try:
        event_features = get_event_features(properties, driver, i)
    except FileNotFoundError as e:
        print("{}   Process={}  {}".format(now(), i, e))

    if event_features is not None:
        write_features(event_features, writer, i, output_file)


def now():
    return time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime())