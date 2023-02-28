class Car:
    # top_speed = 100
    # warnings = []

    # Constructor for scoped to instance attributes (not shared across all instances)
    # __***__ -> double underscore methods aka 'dunder' methods ->> Special methods
    def __init__(c, starting_top_speed=100):
        c.top_speed = starting_top_speed
        # One-sided dunder attribute declarations make the attributes private (inaccessible from any type of function calls outside)
        c.__warnings = []
    

    # Additional functions to add and get warning text from outside the class because the original warnings attribute was made private
    def add_warning(c, warning_text):
        if len(warning_text) > 0:
            c.__warnings.append(warning_text)


    def get_warnings(c):
        return c.__warnings
    

    # Dunder function for typical (general) return value/object
    def __repr__(c):
        print("Printing...")
        return "Top speed: {}, Warnings: {}".format(c.top_speed, len(c.__warnings))
    

    def drive(c):
        print("Driving. Top speed: {}".format(c.top_speed))


car1 = Car()
car1.drive()

# Dunder method __repr__() executed on printing the object without any additional procedures.
print(car1)

# Car.top_speed = 200
# car1.__warnings.append("New warning.")
# Normal appending and printing methods will not work as __warnings is made a private attribute
# Added functions can be used to get the desired attribute-based output
car1.add_warning("New warning.")

# Dunder method for printing attributes of a class as a dictionary
print(car1.__dict__)

car2 = Car(200)
car2.drive()
# print(car2.warnings)
print(car2.get_warnings())

car3 = Car(250)
car3.drive()
# print(car2.warnings)
print(car3.get_warnings())
