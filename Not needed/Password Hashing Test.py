import uuid
import hashlib
true = True

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    print(password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest())
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

new_pass = input('Please enter a password: ')
hashed_password = hash_password(new_pass)
print('The string to store in the db is: ' + hashed_password)

#hashed_password = "d35da1e5f76c84fd96d42a2c55b0f225c373d4f25e1013b50c2716f7a15ad56c:e8efb39c14ee49d3bbc613ad849c79a3"

while true == True:
    old_pass = input('Now please enter the password again to check: ')
    if check_password(hashed_password, old_pass):
        print('You entered the right password')
    else:
        print('I am sorry but the password does not match')
