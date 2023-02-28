class Vehicle:
    
    def __init__(c, starting_top_speed=100):
        c.top_speed = starting_top_speed
        c.__warnings = []
    

    def add_warning(c, warning_text):
        if len(warning_text) > 0:
            c.__warnings.append(warning_text)


    def get_warnings(c):
        return c.__warnings
    

    def __repr__(c):
        print("Printing...")
        return "Top speed: {}, Warnings: {}".format(c.top_speed, len(c.__warnings))
    

    def drive(c):
        print("Driving. Top speed: {}".format(c.top_speed))
