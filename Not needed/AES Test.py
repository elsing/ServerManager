key = "this is my key"
message = "this is my message"

result = b""
last_char = None
for i, message_char in enumerate(message):
    key_char = key[i % len(key)]
    xored_char = ord(message_char) ^ ord(key_char)
    if last_char is not None:
        xored_char ^= last_char

    last_char = xored_char
    result += chr(xored_char).encode('utf-8')



def encrypt(key, message):
    key = key.encode()
    message = message.encode()

    # Divide the message into blocks
    block_size = 8
    blocks = []

encrypt("1234", "12")

print(result)


##def makeVernamCypher( text, key ):
##    """ Returns the Vernam Cypher for given string and key """
##    answer = "" # the Cypher text
##    p = 0 # pointer for the key
##    for char in text:
##        answer += chr(ord(char) ^ ord(key[p]))
##        p += 1
##        if p==len(key):
##            p = 0
##    return answer
##
##                      
##MY_KEY = "cvwopslweinedvq9fnasdlkfn2"
##while True:
##    print("\n\n---Vernam Cypher---")
##    PlainText = input("Enter text to encrypt: ")
##    # Encrypt
##    Cypher = makeVernamCypher(PlainText, MY_KEY)
##    file = open("Key.txt","w")
##    file.write(Cypher)
##    file.close()
##    print("Cypher text: "+Cypher)
##    # Decrypt
##    decrypt = makeVernamCypher(Cypher, MY_KEY)
##    print("Decrypt: "+decrypt)

##"""
##Vernam Cipher
##Benjamin D. Miller
##Takes a key, and a message
##Encripts the message using the key
##"""
##def vernam(key,message):
##    message = str(message)
##    m = message.upper().replace(" ","") # Convert to upper case, remove whitespace
##    encrypt = ""
##    try:
##        key = int(key)           # if the key value is not a number, then run with key = 0
##    except ValueError:
##        key = 0
##    for i in range(len(m)):
##        letter = ord(m[i])-65      # Letters now range 0-25
##        letter = (letter + key)%25 # Alphanumeric + key mod 25 = 0-25
##        letter +=65
##        
##
##        encrypt = encrypt + chr(letter) # Concatenate message
##        
##    return encrypt
##
##""" * TEST CASES * """
##print(vernam(9,"hello world"))
##print(vernam(9,"elliotelliotelliotelliot"))
##print(vernam(14,"TEST_CASE 34!"))
##print(vernam("test","test"))

###!/usr/bin/env python3
##import sys
##import click
##
##def vernam(text, key, return_str=False, alphanumerical=False):
##    if alphanumerical:  # Set conversion aliases to custom functions using variable 'alphanumerics' rather than unicode points
##        alphanumerics = [i for i in "0123456789abcdefghijklmbopqrstuvwxyzABCDEFGHIJKLMBOPQRSTUVWXYZ"]
##        to_num = lambda x: alphanumerics.index(x)
##        to_char = lambda x: alphanumerics[x]
##    else:  # Set conversion aliases to builtins "ord" and "chr" using unicode points
##        to_num = ord
##        to_char = chr
##    
##    bintext = [ to_num(x) for x in text ]  # Convet text to integers
##    binkey = [ to_num(x) for x in key ]  # Convet key to integers
##    
##    for i in range( len(bintext) - len(binkey) ):  # Resize key to length of text
##        binkey.append( binkey[i] )
##    
##    vernamed = [ bintext[i] ^ binkey[i] for i in range(len(bintext)) ]  # XOR vernam operation
##    result = [to_char(i) for i in vernamed]  # Convert back to text
##    
##    if return_str:
##        return "".join(result)
##    
##    return result
##
##@click.command()
##@click.argument("text")
##@click.argument("key")
##@click.option('--string/--list', '-s/-l', "return_str", default=False, help="return as string [default: list]")
##@click.option('--alphanumerical/--unicode', '-a/-u', "alphanumerical", default=False, help="encode alphanumerically [default: use unicode points]")
##def cli(*args, **kwargs): #text, key, return_str, return_long
##    click.echo( vernam(*args, **kwargs) )
##
##if __name__ == "__main__":
##    pass
##
##
##encoded = vernam("super_secret_message", "very_secret_key")
##print(encoded)
##
##decoded = vernam(encoded, "very_secret_key")
##print( "".join(decoded) )
