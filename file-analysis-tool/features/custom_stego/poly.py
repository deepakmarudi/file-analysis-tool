# Function to encrypt data using the Vigenère Cipher (Polyalphabetic Encryption)
def polyalphabetic_encrypt(plain_text, key):
    encrypted_text = []
    key_length = len(key)
    
    # Iterate over each character in the plaintext
    for i, char in enumerate(plain_text):
        # Check if the character is an alphabetic letter
        if char.isalpha():
            # Get the key character corresponding to the current plaintext character
            key_char = key[i % key_length]
            
            # Determine the shift based on the key character (A=0, B=1, C=2, ..., Z=25)
            shift = ord(key_char.lower()) - ord('a')
            
            # Apply the shift (for both uppercase and lowercase)
            if char.islower():
                encrypted_text.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                encrypted_text.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            # If the character is not alphabetic (like spaces or punctuation), just append it as is
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)


# Function to decrypt data using the Vigenère Cipher (Polyalphabetic Decryption)
def polyalphabetic_decrypt(cipher_text, key):
    decrypted_text = []
    key_length = len(key)
    
    # Iterate over each character in the ciphertext
    for i, char in enumerate(cipher_text):
        # Check if the character is an alphabetic letter
        if char.isalpha():
            # Get the key character corresponding to the current ciphertext character
            key_char = key[i % key_length]
            
            # Determine the shift based on the key character (A=0, B=1, C=2, ..., Z=25)
            shift = ord(key_char.lower()) - ord('a')
            
            # Reverse the shift (for both uppercase and lowercase)
            if char.islower():
                decrypted_text.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            else:
                decrypted_text.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            # If the character is not alphabetic (like spaces or punctuation), just append it as is
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

"""
# Example Usage
if __name__ == "__main__":
    # Example plaintext and key
    data = "This is a secret message!"
    key = "KEY"
    
    # Encrypt the data
    encrypted_data = polyalphabetic_encrypt(data, key)
    print("Encrypted Data:", encrypted_data)
    
    # Decrypt the data
    decrypted_data = polyalphabetic_decrypt(encrypted_data, key)
    print("Decrypted Data:", decrypted_data)
"""
