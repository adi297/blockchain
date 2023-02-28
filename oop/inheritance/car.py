from vehicle import Vehicle

class Car(Vehicle):

    # Class-specific attributes/methods can be added to the class besides the inherited attributes/methods
    def brag(c):
        print("This car reaches {} km/hr!".format(c.top_speed))

car1 = Car()
car1.drive()


print(car1)

car1.add_warning("New warning.")

print(car1.__dict__)
print(car1.get_warnings())
car1.brag()

car2 = Car(200)
car2.drive()
print(car2.get_warnings())
car2.brag()

car3 = Car(250)
car3.drive()
print(car3.get_warnings())
car3.brag()
