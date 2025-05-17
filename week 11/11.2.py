class Model(object):
    services = {
        'email': {'number': 1000, 'price': 2},
        'sms': {'number': 1000, 'price': 10},
        'voice': {'number': 1000, 'price': 15},
    }

class View(object):  # English view
    def list_services(self, services):
        for svc in services:
            print(svc)

    def list_pricing(self, services):
        for svc in services:
            print(f"For {Model.services[svc]['number']} {svc} message you pay $ {Model.services[svc]['price']}")

class View2(object):  # Indonesian view
    def list_services(self, services):
        print("Layanan yang disediakan:")
        for svc in services:
            print(svc)

    def list_pricing(self, services):
        print("Tarif tiap layanan:")
        for svc in services:
            print(f"Untuk setiap {Model.services[svc]['number']} {svc} anda membayar $ {Model.services[svc]['price']}")

class Controller(object):
    def __init__(self):
        self.model = Model()

        print("What language do you choose? [1]English [2]Indonesia: ", end='')
        choice = input()

        if choice == "1":
            self.view = View()
        elif choice == "2":
            self.view = View2()
        else:
            print("Error, choose the language number!")
            exit()

    def get_services(self):
        services = self.model.services.keys()
        self.view.list_services(services)

    def get_pricing(self):
        services = self.model.services.keys()
        self.view.list_pricing(services)

# Main
controller = Controller()
print("\nServices Provided:" if isinstance(controller.view, View) else "")
controller.get_services()

print("\nPricing for Services:" if isinstance(controller.view, View) else "")
controller.get_pricing()
