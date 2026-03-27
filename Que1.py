# HIT137 Assignment 2 - Question 1
# Text Encryption, Decryption and Verification Program


def encrypt_text(shift1, shift2):
    """
    Reads raw_text.txt, encrypts every letter using the rules below,
    and saves the result to encrypted_text.txt.

    Encryption rules:
      Lowercase:
        a-m  -> shift FORWARD  by (shift1 * shift2) positions
        n-z  -> shift BACKWARD by (shift1 + shift2) positions
      Uppercase:
        A-M  -> shift BACKWARD by shift1 positions
        N-Z  -> shift FORWARD  by (shift2 ** 2) positions
      Everything else (numbers, spaces, punctuation) stays the same.
    """

    # Open the original file and read everything in
    with open("raw_text.txt", "r") as f:
        original = f.read()

    encrypted = []  # We'll build the encrypted text character by character

    for char in original:

        # --- lowercase letters ---
        if char.islower():
            # Find where this letter sits in the alphabet (0 = 'a', 25 = 'z')
            pos = ord(char) - ord('a')

            if pos <= 12:   # a-m: first half → shift forward
                new_pos = (pos + shift1 * shift2) % 26
            else:           # n-z: second half → shift backward
                new_pos = (pos - (shift1 + shift2)) % 26

            encrypted.append(chr(new_pos + ord('a')))

        # --- uppercase letters ---
        elif char.isupper():
            pos = ord(char) - ord('A')

            if pos <= 12:   # A-M: first half → shift backward
                new_pos = (pos - shift1) % 26
            else:           # N-Z: second half → shift forward by shift2 squared
                new_pos = (pos + shift2 ** 2) % 26

            encrypted.append(chr(new_pos + ord('A')))

        # --- anything else: leave it exactly as is ---
        else:
            encrypted.append(char)

    # Join all the characters back into one string and write the file
    encrypted_text = "".join(encrypted)
    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted_text)

    print("Encryption done! Saved to encrypted_text.txt")


def decrypt_text(shift1, shift2):
    """
    Reads encrypted_text.txt and reverses the encryption to recover
    the original text, saving it to decrypted_text.txt.

    We simply do the opposite operation for each rule:
      Lowercase a-m  was shifted FORWARD  → now shift BACKWARD
      Lowercase n-z  was shifted BACKWARD → now shift FORWARD
      Uppercase A-M  was shifted BACKWARD → now shift FORWARD
      Uppercase N-Z  was shifted FORWARD  → now shift BACKWARD
    """

    with open("encrypted_text.txt", "r") as f:
        encrypted = f.read()

    decrypted = []

    for char in encrypted:

        # --- lowercase letters ---
        if char.islower():
            pos = ord(char) - ord('a')

            # We need to figure out which half this letter originally came from.
            # After encryption, letters that were a-m moved forward by (shift1*shift2).
            # We reverse-check by shifting back and seeing if the result lands in a-m.
            original_pos_if_first_half = (pos - shift1 * shift2) % 26
            original_pos_if_second_half = (pos + (shift1 + shift2)) % 26

            # If undoing the first-half rule puts us back in a-m, that's correct
            if original_pos_if_first_half <= 12:
                new_pos = original_pos_if_first_half
            else:
                new_pos = original_pos_if_second_half

            decrypted.append(chr(new_pos + ord('a')))

        # --- uppercase letters ---
        elif char.isupper():
            pos = ord(char) - ord('A')

            original_pos_if_first_half = (pos + shift1) % 26
            original_pos_if_second_half = (pos - shift2 ** 2) % 26

            # If undoing the first-half rule puts us back in A-M, that's correct
            if original_pos_if_first_half <= 12:
                new_pos = original_pos_if_first_half
            else:
                new_pos = original_pos_if_second_half

            decrypted.append(chr(new_pos + ord('A')))

        # --- leave non-letters alone ---
        else:
            decrypted.append(char)

    decrypted_text = "".join(decrypted)
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted_text)

    print("Decryption done! Saved to decrypted_text.txt")


def verify_decryption():
    """
    Compares raw_text.txt with decrypted_text.txt to check
    whether the decryption perfectly recovered the original.
    Prints a clear success or failure message.
    """

    with open("raw_text.txt", "r") as f:
        original = f.read()

    with open("decrypted_text.txt", "r") as f:
        decrypted = f.read()

    if original == decrypted:
        print("Verification PASSED ✓ - Decrypted text matches the original perfectly!")
    else:
        print("Verification FAILED ✗ - The texts do not match.")

        # Give a hint about where the first difference is so it's easier to debug
        for i, (a, b) in enumerate(zip(original, decrypted)):
            if a != b:
                print(f"  First difference at position {i}: "
                      f"original={repr(a)}, decrypted={repr(b)}")
                break


# -----------------------------------------------------------------------
# Main program - this runs when you execute the script directly
# -----------------------------------------------------------------------
if __name__ == "__main__":

    # Step 1: Ask the user for the two shift values
    print("=== HIT137 Assignment 2 - Question 1 ===\n")

    while True:
        try:
            shift1 = int(input("Enter shift1 (a whole number): "))
            shift2 = int(input("Enter shift2 (a whole number): "))
            break   # Both inputs are valid integers, move on
        except ValueError:
            print("Please enter whole numbers only.\n")

    print()  # blank line for readability

    # Step 2: Encrypt
    encrypt_text(shift1, shift2)

    # Step 3: Decrypt
    decrypt_text(shift1, shift2)

    # Step 4: Verify
    verify_decryption()