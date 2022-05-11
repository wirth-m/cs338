# McKenna Wirth and Antonia Ritter 
# CS338 Spring 2022
# BRUTE-FORCE PASSWORD CRACKING


import hashlib
import binascii
from collections import defaultdict



# Input: filename for (unsalted) password file
# Returns: dictionary where key = hash and val = username 
def import_passwords(filename):
    passwords_dict = defaultdict(list) 
    for line in open(filename):
        username = line.split(":")[0]
        password_hash = line.split(":")[1]
        passwords_dict[password_hash].append(username)
    return passwords_dict



# Input: filename for salted password file
# Returns: dictionary where key = hash and val = [username, salt] (a list)
def import_salted_passwords(filename):
    salted_passwords_dict = defaultdict(str)
    salt_list = []
    for line in open(filename):
        username = line.split(":")[0]
        salt = line.split("$")[2]
        rest_of_line = line.split("$")[3]
        salted_hash = rest_of_line.split(":")[0]
        salted_passwords_dict[salted_hash] = [username, salt]
        salt_list.append(salt)
    return salted_passwords_dict, salt_list



# Modified from Jeff's conversions.py
# Input: a string 
# Output: SHA-256 hash 
def string_to_hash(password_as_string):
    password = password_as_string # type=string
    encoded_password = password.encode('utf-8') # type=bytes
    hasher = hashlib.sha256(encoded_password)
    digest = hasher.digest() # type=bytes
    digest_as_hex = binascii.hexlify(digest) # weirdly, still type=bytes
    digest_as_hex_string = digest_as_hex.decode('utf-8') # type=string
    return digest_as_hex_string



# Phase 1 
# Writes passwords to cracked1.txt after all words have been checked 
# This is fine because this one takes < 1 sec 
def passwords1(words):
    passwords_cracked = 0
    hashes_computed = 0 
    cracked_passwords = defaultdict(str)
    passwords_dict = import_passwords("passwords1.txt")

    # Loop over possible passwords 
    for word in words:
        # Convert to hash 
        hash = string_to_hash(word) 
        hashes_computed += 1 
        # Check against passwords_dict 
        if passwords_dict.get(hash) != None:
            # Accounting for repeat passwords
            for username in passwords_dict.get(hash):
                cracked_passwords[username] = word
                passwords_cracked += 1 

    # Output to file 
    with open('cracked1.txt', 'w') as f:
        for key in sorted(cracked_passwords.keys()):
            out_string = f"{key}:{cracked_passwords[key]}\n"
            f.write(out_string)

    print(f"    Passwords cracked: {passwords_cracked}")
    print(f"    Hashes computed: {hashes_computed}")



# Phase 2
# Writes passwords to file once all pairs of words have been 
# checked OR program is killed 
# Which it is bc this takes ~2 days 
def passwords2(words):
    passwords_cracked = 0
    hashes_computed = 0 
    passwords_dict = import_passwords("passwords2.txt")

    f = open('cracked2.txt', 'w')

    # loop over possible passwords 
    words_plus_empty_string = [""] + words
    # insert the empty string to check all single words first 
    for word1 in words_plus_empty_string: 
        print(word1)
        for word2 in words:
            # convert to hash 
            hash = string_to_hash(word1+word2) 
            hashes_computed += 1 
            # check against passwords_dict 
            if passwords_dict.get(hash) != None:
                passwords_cracked += 1 
                username = passwords_dict[hash]

                # Progress report 
                print(username, word1+word2)
                print(f"    Passwords cracked: {passwords_cracked}")
                print(f"    Hashes computed: {hashes_computed}")

                # write to file 
                out_string = f"{username}:{word1+word2}\n"
                f.write(out_string)

    # if you kill the code before it finishes Python automatically 
    # closes and writes all passwords so far to the file 
    f.close() 



# Phase 3 
# Writes passwords to file once all pairs of words have been 
# checked OR program is killed 
# This takes about 15 minutes 
def passwords3(words):
    passwords_cracked = 0
    hashes_computed = 0
    passwords_dict, salt_list = import_salted_passwords("passwords3.txt")
    num_passwords = len(salt_list)
    print(f"There are {num_passwords} passwords to crack.\n")

    f = open('cracked3.txt', 'w')

    # Note: these passwords are all single words 
    # Loop over possible passwords
    for word1 in words:
        # Loop over all salts 
        for salt in salt_list:
            # Check if salt+password -> hash in passwords_dict 
            hash = string_to_hash(salt+word1)
            hashes_computed += 1
            if passwords_dict.get(hash) != None:
                passwords_cracked += 1
                username = passwords_dict[hash][0]

                # Progress report 
                print(username, word1)
                print(f"    Passwords cracked: {passwords_cracked}")
                print(f"    Hashes computed: {hashes_computed}")

                out_string = f"{username}:{word1}\n"
                f.write(out_string)
    f.close()



def main():
    words = [line.strip().lower() for line in open('words.txt')]
    passwords1(words)
    # passwords2(words)
    # passwords3(words)



if __name__=="__main__":
    main()