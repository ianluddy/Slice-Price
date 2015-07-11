from slice_scanner.objects.vendor import Vendor

class PapaJohns(Vendor):

    id = "papa_johns"
    name = "Papa Johns"
    site = "https://www.papajohns.co.uk/"

    diameter_reference = {
    }

    slice_reference = {
    }

    def _get_meals(self):
        return []

    def _get_desserts(self):
        return []

    def _get_sides(self):
        return []

    def _get_pizzas(self):
        return []

    def _login(self):
        return None