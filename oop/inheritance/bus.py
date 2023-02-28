from vehicle import Vehicle

class Bus(Vehicle):

    # Only creating a new constructer will overwrite the inherited constructor.
    # THe super() method can be used to inherit the parent class constructor attributes in the contruction of the new constructor
    def __init__(c, starting_top_speed=100):
        super().__init__(starting_top_speed)
        c.passengers = []


    def add_passengers(c, passengers):
        c.passengers.extend(passengers)

bus1 = Bus()
bus1.drive()


print(bus1)

bus1.add_warning("New warning.")

print(bus1.__dict__)
print(bus1.get_warnings())
bus1.add_passengers(['a', 'b', 'c'])
print(bus1.passengers)

bus2 = Bus(200)
bus2.drive()
print(bus2.get_warnings())
bus2.add_passengers(['d', 'e', 'f'])
print(bus2.passengers)


bus3 = Bus(250)
bus3.drive()
print(bus3.get_warnings())
bus3.add_passengers(['f', 'g', 'h'])
print(bus3.passengers)
