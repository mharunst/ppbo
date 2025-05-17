class Model(object):
    services = {
        'email': {'number': 1000, 'price': 2},
        'sms': {'number': 1000, 'price': 10},
        'voice': {'number': 1000, 'price': 15},
    }

class View(object):  # English view only
    def list_services(self, services):
        print("Services Provided:")
        for svc in services:
            print(svc)

    def list_pricing(self, services):
        print("\nPricing for Services:")
        for svc in services:
            print(f"For {Model.services[svc]['number']} {svc} message you pay $ {Model.services[svc]['price']}")

class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View()

    def get_services(self):
        services = self.model.services.keys()
        self.view.list_services(services)

    def get_pricing(self):
        services = self.model.services.keys()
        self.view.list_pricing(services)

    def bid_price(self):
        print("\nWhat service do you want to bid? email, sms, or voice: ", end='')
        tawar = input()
        if tawar not in self.model.services:
            print("Invalid service!")
            return

        print("Enter the price you want (in $): ", end='')
        try:
            harga = float(input())
            self.model.services[tawar]['price'] = harga
            print("\nPrice according to your bid!")
            self.get_pricing()
        except ValueError:
            print("Invalid input. Please enter a numeric value for the price.")

# Main Program
controller = Controller()
controller.get_services()
controller.get_pricing()
controller.bid_price()

