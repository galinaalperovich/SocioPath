from selenium import webdriver

from settings import path_to_phantomjs


class FeatureExtractor:
    def __init__(self, micro_property):
        """

        :type micro_property: MicroProperty
        """
        self.micro_property = micro_property

        self.depth_until_me = self.__get_depth_until_me()
        self.num_childs = self.__get_num_childs()
        self.depth_until_me = self.__get_depth_after_me()

        self.line = self.__get_line()

        self.tag = self.__get_tag()

        self.text = micro_property.value
        self.text_density = self.__get_text_density()

        self.xy_coords = self.__get_xy_coords()
        self.block_size = self.__get_block_size()

        self.classes = self.__get_css_classes()
        self.css_prop = self.__get_css_properties()
        self.css_font = self.__get_css_font()
        self.css_color = self.__get_css_color()
        self.css_weight = self.__get_css_weight()

        self.driver = webdriver.PhantomJS(executable_path=path_to_phantomjs)
        self.driver.get(self.micro_property.url)

        self.webelement = self.__get_web_element()

    def __get_depth_until_me(self):
        return None

    def __get_num_childs(self):
        return None

    def __get_depth_after_me(self):
        return None

    def __get_line(self):
        return None

    def __get_tag(self):
        return None

    def __get_text_density(self):
        return None

    def __get_xy_coords(self):
        return None

    def __get_block_size(self):
        return None

    def __get_css_classes(self):
        return None

    def __get_css_properties(self):
        return None

    def __get_css_font(self):
        return None

    def __get_css_color(self):
        return None

    def __get_css_weight(self):
        return None

    def __get_web_element(self):
        driver = self.driver

        my_scope = self.micro_property.scope
        xpath_scope = "//*[@itemscope][@itemtype='{}']".format(my_scope)
        scope_element = driver.find_elements_by_xpath(xpath_scope).pop()

        name = self.micro_property.name
        values_elements = set(
            scope_element.find_elements_by_xpath(".//*[@itemprop='{}']".format(name)))

        scopes = driver.find_elements_by_xpath("//*[@itemscope]")
        except_elements = set()
        for scope in scopes:
            type = scope.get_attribute('itemtype')

            if type == my_scope:
                continue
            els = scope.find_elements_by_xpath(".//*[@itemprop='{}']".format(name))
            for el in els:
                except_elements.add(el)

        one_element = values_elements.difference(except_elements).pop()

        return one_element
