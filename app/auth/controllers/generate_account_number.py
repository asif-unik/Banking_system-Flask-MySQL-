import time
import random



def generate_account_number():
    # Generate a timestamp (current time in milliseconds)
    timestamp = int(time.time())   
    # Generate a random 4-digit number
    random_number = random.randint(1000, 9999)  
    # Combine timestamp and random number to form a 14-digit account number
    account_number = int(f"{timestamp}{random_number}")  
    return account_number
