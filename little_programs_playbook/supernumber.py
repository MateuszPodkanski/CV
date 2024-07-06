class number:

    def __init__(self,number : int):
        # moglibyśmy zrobić tutaj dodatkowo walidacje wprowadzanej liczby sprawdzającej czy nie 
        # dostajemy liter lub floata zamiast tego użyłem po prostu typingu jako że przy błędnej wartości błąd i tak wyskoczy
        self.number = number
        self.abs_number = self.convert_to_abs()
        self.supernumber = self.sum_digits()
    
    def convert_to_abs(self):
        converted_number = abs(self.number)
        return converted_number
        
    def sum_digits(self):
        return sum(int(digit) for digit in str(self.abs_number))
        
    def __str__(self):
        return f"Supernumber for this value is {self.supernumber}"

# I created a lot of functions instead of one to mantain SOLID, for easier testing, understading code, fixing bugs etc. 
# and class is actually usefull in here for creating difference hardcoded instances

# We could also obviously create inputs for the user to provide us code and also create 

first_number = number(123)
print(first_number)

second_number = number(92834)
print(second_number)

third_number = number(-123123)
print(third_number)