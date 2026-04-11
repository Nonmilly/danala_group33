# HIT137 Assignment 2 - Question 1
# Encrypts a text file, decrypts it, then verifies they match

import os

# shift a character within its specific group of 13 letters
# this keeps a-m inside a-m, n-z inside n-z etc. so decryption always works
def shift_in_group(char, amount, group_start):
    pos = ord(char) - ord(group_start)
    new_pos = (pos + amount) % 13   # wrap within 13-letter group only
    return chr(ord(group_start) + new_pos)

# encrypt one character using the assignment rules
def encrypt_char(ch, shift1, shift2):
    if not ch.isalpha():
        return ch  # numbers, spaces, punctuation unchanged

    if ch.islower():
        if 'a' <= ch <= 'm':
            return shift_in_group(ch, shift1 * shift2, 'a')   # shift forward
        else:
            return shift_in_group(ch, -(shift1 + shift2), 'n') # shift backward

    else:
        if 'A' <= ch <= 'M':
            return shift_in_group(ch, -shift1, 'A')            # shift backward
        else:
            return shift_in_group(ch, shift2 ** 2, 'N')        # shift forward by shift2 squared

# decrypt one character - just reverse the shift within the same group
def decrypt_char(ch, shift1, shift2):
    if not ch.isalpha():
        return ch

    if ch.islower():
        if 'a' <= ch <= 'm':
            return shift_in_group(ch, -(shift1 * shift2), 'a')
        else:
            return shift_in_group(ch, +(shift1 + shift2), 'n')

    else:
        if 'A' <= ch <= 'M':
            return shift_in_group(ch, +shift1, 'A')
        else:
            return shift_in_group(ch, -(shift2 ** 2), 'N')


# reads raw_text.txt and writes encrypted content to encrypted_text.txt
def encrypt(shift1, shift2):
    with open('raw_text.txt', 'r') as f:
        text = f.read()

    encrypted = ''.join(encrypt_char(c, shift1, shift2) for c in text)

    with open('encrypted_text.txt', 'w') as f:
        f.write(encrypted)

    print("Encrypted successfully -> encrypted_text.txt")


# reads encrypted_text.txt and writes decrypted content to decrypted_text.txt
def decrypt(shift1, shift2):
    with open('encrypted_text.txt', 'r') as f:
        text = f.read()

    decrypted = ''.join(decrypt_char(c, shift1, shift2) for c in text)

    with open('decrypted_text.txt', 'w') as f:
        f.write(decrypted)

    print("Decrypted successfully -> decrypted_text.txt")


# compares raw_text.txt and decrypted_text.txt to confirm they match
def verify():
    with open('raw_text.txt', 'r') as f:
        original = f.read()
    with open('decrypted_text.txt', 'r') as f:
        decrypted = f.read()

    if original == decrypted:
        print("Verification passed - decrypted text matches the original!")
    else:
        print("Verification failed - files do not match.")


# --- main ---
if __name__ == '__main__':
    print("=== HIT137 Assignment 2 - Question 1 ===\n")

    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))
    print()

    encrypt(shift1, shift2)
    decrypt(shift1, shift2)
    verify()

 