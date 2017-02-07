class JSCodeEmbedder():
    @property
    def get_xpath_by_xy(self):
        """
        This is javascript code which returns XPath by X, Y position.
        Function is written for selenium webdriver.
        Example of use:

        driver = webdriver.PhantomJS()
        driver.get("google.com")
         driver.execute_script(get_xpath_by_xy, 100, 100)

        :return:
        """
        return """
        function getPathTo(element) {
            if (element.id!=='')
                return 'id("'+element.id+'")';
            if (element===document.body)
                return element.tagName;

            var ix= 0;
            var siblings= element.parentNode.childNodes;
            for (var i= 0; i<siblings.length; i++) {
                var sibling = siblings[i];
                if (sibling===element)
                    return getPathTo(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
                if (sibling.nodeType===1 && sibling.tagName===element.tagName)
                    ix++;
            }
        }

        var element = document.elementFromPoint(arguments[0], arguments[1]);
        return getPathTo(element);
        """
