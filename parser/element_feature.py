from parser.javascript_functions import get_all_css_properties, get_xpath_by_element


class ElementFeature:
    def __init__(self, element_property, driver):
        self.url = element_property.url
        self.driver = driver
        self.driver.get(self.url.strip())
        self.webelement = element_property.element
        self.xpath = driver.execute_script(get_xpath_by_element(), self.webelement)
        self.num_childs = self.__get_num_childs()
        self.num_siblings = self.__get_num_siblings()

        self.tag = self.__get_tag()

        self.text_property = self.__get_text_property(self.webelement.text)

        self.xy_coords = self.__get_xy_coords()
        self.block_size = self.__get_block_size()

        self.classes = self.__get_css_classes()
        self.css_prop = self.__get_css_properties()

    def __get_num_childs(self):

        try:
            self.driver.execute_script(
                "return arguments[0].children.length;", self.webelement)
        except Exception as e:
            return None

    def __get_tag(self):
        return self.webelement.tag_name if self.webelement else None

    def __get_xy_coords(self):
        return self.webelement.location if self.webelement else None

    def __get_block_size(self):
        return self.webelement.size if self.webelement else None

    def __get_css_classes(self):
        try:
            return self.driver.execute_script("return arguments[0].className.split(' ')", self.webelement)
        except Exception as e:
            return None

    def __get_css_properties(self):
        try:
            node = self.driver.find_element_by_xpath(self.xpath)
            return self.driver.execute_script(
                get_all_css_properties(), node)
        except Exception as e:
            return None

    def __get_xpath(self):
        return self.driver.execute_script(get_xpath_by_element(), self.webelement)

    def __get_num_siblings(self):
        try:
            return self.driver.execute_script(
                "var temp = arguments[0].parentNode; child = temp.children; return child.length;", self.webelement)
        except Exception as e:
            return None

    def __get_text_property(self, text):
        return text.replace('\t', ' ').replace('\n', ' ')
