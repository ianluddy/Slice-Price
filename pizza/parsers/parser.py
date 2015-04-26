__author__ = 'ianluddy'

class Parser():

    def _login(self):
        pass

    def _get_pizzas(self):
        pass

    def _parse_pizzas(self):
        pass

    def _get_meals(self):
        pass

    def _parse_meals(self):
        pass

    def get_pizzas(self):
        self._login()
        return self._parse_pizzas(self._get_pizzas())
