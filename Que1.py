# HIT137 Assignment 2 - Question 1
# Text Encryption, Decryption and Verification Program


def encrypt_char(char, shift1, shift2):
    """
    Encrypts a single character using the assignment rules.
    Returns the encrypted character.

    Lowercase:
      a-m  → shift FORWARD  by (shift1 * shift2) positions (wraps within alphabet)
      n-z  → shift BACKWARD by (shift1 + shift2) positions (wraps within alphabet)
    Uppercase:
      A-M  → shift BACKWARD by shift1 positions
      N-Z  → shift FORWARD  by (shift2 ** 2) positions
    Everything else stays the same.
    """

    if char.islower():
        pos = ord(char) - ord('a')          # 0 for 'a', 25 for 'z'
        if pos <= 12:                        # a-m: first half
            new_pos = (pos + shift1 * shift2) % 26
        else:                                # n-z: second half
            new_pos = (pos - (shift1 + shift2)) % 26
        return chr(new_pos + ord('a'))

    elif char.isupper():
        pos = ord(char) - ord('A')
        if pos <= 12:                        # A-M: first half
            new_pos = (pos - shift1) % 26
        else:                                # N-Z: second half
            new_pos = (pos + shift2 ** 2) % 26
        return chr(new_pos + ord('A'))

    else:
        return char                          # spaces, numbers, punctuation unchanged


def decrypt_char(char, shift1, shift2):
    """
    Decrypts a single character by reversing the encryption.

    The key insight: we try BOTH possible reversals and pick the one
    whose ORIGINAL position matches the half that would have produced it.

    For example, if a lowercase letter was originally in a-m (pos 0-12),
    it was shifted FORWARD. So we undo that by shifting BACKWARD,
    and then CHECK that the result actually lands back in 0-12.
    If it does, we have the right answer. Otherwise, it must have
    come from n-z, so we undo that rule instead.
    """

    if char.islower():
        pos = ord(char) - ord('a')

        # Try reversing the a-m rule (undo forward shift)
        candidate_first = (pos - shift1 * shift2) % 26
        if candidate_first <= 12:
            # The original was in a-m, and undoing the shift lands back there ✓
            return chr(candidate_first + ord('a'))
        else:
            # Must have come from n-z (undo backward shift)
            candidate_second = (pos + (shift1 + shift2)) % 26
            return chr(candidate_second + ord('a'))

    elif char.isupper():
        pos = ord(char) - ord('A')

        # Try reversing the A-M rule (undo backward shift)
        candidate_first = (pos + shift1) % 26
        if candidate_first <= 12:
            # The original was in A-M ✓
            return chr(candidate_first + ord('A'))
        else:
            # Must have come from N-Z (undo forward shift)
            candidate_second = (pos - shift2 ** 2) % 26
            return chr(candidate_second + ord('A'))

    else:
        return char


def encrypt_text(shift1, shift2):
    """
    Reads raw_text.txt, encrypts every character,
    and saves the result to encrypted_text.txt.
    """

    with open("raw_text.txt", "r") as f:
        original = f.read()

    # Encrypt each character one by one
    encrypted = "".join(encrypt_char(c, shift1, shift2) for c in original)

    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted)

    print("Encryption done! Saved to encrypted_text.txt")


def decrypt_text(shift1, shift2):
    """
    Reads encrypted_text.txt, decrypts every character,
    and saves the result to decrypted_text.txt.
    """

    with open("encrypted_text.txt", "r") as f:
        encrypted = f.read()

    # Decrypt each character one by one
    decrypted = "".join(decrypt_char(c, shift1, shift2) for c in encrypted)

    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted)

    print("Decryption done! Saved to decrypted_text.txt")


def verify_decryption():
    """
    Compares raw_text.txt with decrypted_text.txt.
    Prints PASSED if they are identical, FAILED if not.
    """

    with open("raw_text.txt", "r") as f:
        original = f.read()

    with open("decrypted_text.txt", "r") as f:
        decrypted = f.read()

    if original == decrypted:
        print("Verification PASSED - Decrypted text matches the original perfectly!")
    else:
        print("Verification FAILED - The texts do not match.")

        # Point out exactly where the first difference is to help with debugging
        for i, (a, b) in enumerate(zip(original, decrypted)):
            if a != b:
                print(f"  First difference at position {i}: "
                      f"original={repr(a)}, decrypted={repr(b)}")
                break


# -----------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------
if __name__ == "__main__":

    print("=== HIT137 Assignment 2 - Question 1 ===\n")

    # Keep asking until the user gives two valid whole numbers
    while True:
        try:
            shift1 = int(input("Enter shift1 (a whole number): "))
            shift2 = int(input("Enter shift2 (a whole number): "))
            break
        except ValueError:
            print("Please enter whole numbers only.\n")

    print()

    encrypt_text(shift1, shift2)   # Step 1: encrypt raw_text.txt
    decrypt_text(shift1, shift2)   # Step 2: decrypt encrypted_text.txt
    verify_decryption()            # Step 3: confirm the result matches original