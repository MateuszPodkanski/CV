class Palindrome:
    
    def __init__(self):
        self.word = self.get_value_str("Please provide me word for Palindrome checking: ")
        self.result = self.palindrome_check()
    
    def palindrome_check(self):
        return self.word == self.word[::-1]
    

#instead of input we could obviously hardcore words into the class when calling it depending on the case
    def get_value_str(self,communicate : str):
        while True:
            word = input(communicate).strip()
            if word:
                return word
            else:
                print("Input cannot be empty. Please enter a proper word.")
    
    def palindrome_result(self):
        if self.result:
            print("Word is a palindrome")
        else:
            print("Word is not a palindrome")

# we could put a loop in here to check more words one by one

while True:

    palindrome = Palindrome()
    palindrome.palindrome_result()

    continue_check = input("Do you want to check another word? (yes/no): ").strip().lower()
    if continue_check != 'yes':
        break

# Please note that I know that without class code would be shorter and as this is exercise which 
# won't be extended there is no need to create classes or even functions/methods
# but I wanted to show I can build things like that which is more advanced overall
