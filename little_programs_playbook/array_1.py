class Array:

    def __init__(self,array : list):
        self.check_if_list(array)
        self.check_if_elements_int(array)
        self.array = array
        self.sorted_array = self.sort_array()
        self.min_sum = self.min_sum()
        self.max_sum = self.max_sum()

    @staticmethod
    def check_if_list(array):
        if not isinstance(array,list):
            raise TypeError("Input must be a list")

    @staticmethod
    def check_if_elements_int(array):
        for element in array:
            if not isinstance(element,int):
                raise TypeError("All elements of the list should be integers")

    def sort_array(self):
        sorted_array = self.array.sort()
        return sorted_array


    def min_sum(self):
        min_sum = sum(self.array[:4])
        return min_sum

    def max_sum(self):
        max_sum = sum(self.array[-4:])
        return max_sum
    
    def __str__(self):
        return f"Min is {self.min_sum}, and max is {self.max_sum}."

array_1 = Array([1,2,3,4,5])
print(array_1)

array_2 = Array([3,8,10,2,11])
print(array_2)

array_3 = Array ([3,28,3,"a",2])
print(array_3)
