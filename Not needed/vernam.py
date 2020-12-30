def vernam(text, key, return_str=False, alphanumerical=False):
    #Code by "roysoup"
    if alphanumerical:
        alphanumerics = [i for i in "0123456789abcdefghijklmbopqrstuvwxyzABCDEFGHIJKLMBOPQRSTUVWXYZ"]
        to_num = lambda x: alphanumerics.index(x)
        to_char = lambda x: alphanumerics[x]
    else:  
        to_num = ord
        to_char = chr
    
    bintext = [ to_num(x) for x in text ]  
    binkey = [ to_num(x) for x in key ]  
    
    for i in range( len(bintext) - len(binkey) ):  # Resize key to length of text
        binkey.append( binkey[i] )
    
    vernamed = [ bintext[i] ^ binkey[i] for i in range(len(bintext)) ]  # XOR vernam operation
    result = [to_char(i) for i in vernamed]  # Convert back to text
    
    if return_str:
        return "".join(result)
    #Code by "roysoup" done

    final = ""
    for i in range(0,len(result)):
        final += result[i]
    return final


def checkPassword(hashedPassword, userPassword):
    password, salt = hashedPassword.split(':')
    return password == hashlib.sha256(salt.encode() + userPassword.encode()).hexdigest()

passW = vernam("Provides a Windows Server machine connected to AD for connection. Also runs minor services like the UniFi Web Interface.", "1234")

print(passW)

#print(checkPassword(passW, "1234"))