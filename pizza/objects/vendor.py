import abc
from ..objects.pizza import Pizza
from ..utils import make_uuid
from selenium import webdriver

class Vendor():
    __metaclass__  = abc.ABCMeta

    # Toppings normaliser. For converting things like "Smoked Bacon Rashers" to "bacon"
    toppings = {}
    # web_driver = webdriver.Firefox()
    web_driver = webdriver.Chrome('C:\\chromeDRIVER.exe', service_args=['--ignore-ssl-errors=true'])
    # web_driver = webdriver.PhantomJS('C:\\phantomjs.exe', service_args=['--ignore-ssl-errors=true'])

    def __init__(self):
        self.name = self.__class__.__name__
        self.id = make_uuid(self.__class__.__name__)

    def _normalise_toppings(self, topping_list):
        return sorted([self._normalise_topping(topping) for topping in topping_list])

    def _normalise_topping(self, topping):
        return self.toppings[topping] if topping in self.toppings else topping

    def _new_pizza(self, name, toppings, size, diameter, price, base, slices):
        return Pizza(self.id, name, self._normalise_toppings(toppings), size, diameter, price, base, slices)

    #### Implement ####

    @abc.abstractmethod
    def get_pizzas(self):
        """ Get list of Pizzas """

    @abc.abstractmethod
    def get_meals(self):
        """ Get list of Meals """

    @abc.abstractmethod
    def get_sides(self):
        """ Get list of Sides """

    @abc.abstractmethod
    def get_desserts(self):
        """ Get list of Desserts """

