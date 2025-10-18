import sys # it imports necessary modules like system fxn(like:-exiting the program) 
import os # it imports necessary modules like operating system fxn(like:- checking for files)
from cryptography.fernet import Fernet # fernet is the class the provides the secure encryption methods
KEY_FILE = "secret.key" #  it define as global variable holding the name of the file where the "secret key" will be stored
"""
Explanation from(Line No-11 to Line No-16):-
try and except used to handle the ImportError exception that may occur if the 'cryptography' package is not installed in the Python environment.
If the import fails, a user-friendly message is printed to inform the user about the missing dependency and how to install it using pip. Finally,
 the program exits gracefully using sys.exit(1) to indicate an error condition.
"""
try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Missing dependency: the 'cryptography' package is not installed.")
    print("Install it with: python -m pip install cryptography")
    sys.exit(1)
"""
Explanation from(Line No-21&22):-
it defines a function to crate a new random encryption key using Fernet's built-in key generation method.
"""
def generate_key():
   return Fernet.generate_key()
"""
Explanation from(Line No-27 to Line No-38):-
it starts the definiton of the central function that either loads an existing encryption key from a file or generates a new one if the file does not exist.
"""
def load_or_generate_key():    
    if os.path.exists(KEY_FILE):  # Uses the os.path.exists function to check if the file defined by KEY_FILE (secret.key) already exists in the current directory.       
        with open(KEY_FILE, "rb") as key_file: # If the file exists, it opens the file in binary read mode ("rb") using a with statement to ensure proper file handling.
            key = key_file.read()
        print(f"Key loaded successfully from '{KEY_FILE}'.")
        return key
    else: # Executes if secret.key was not found.
        key = generate_key() # Calls the function defined on line 11 to create a brand new key.
        with open(KEY_FILE, "wb") as key_file: # Opens a new file named secret.key in write binary mode ("wb") and writes the newly generated key into it.
            key_file.write(key)
        print(f"New key generated and saved to '{KEY_FILE}'. (Keep this file secure!)")
        return key
""""
Explanation from(Line No-43 to Line No-53):-
it defines two functions: one for encrypting a message and another for decrypting it using the provided key.
"""
def encrypt_message(message: str, key: bytes) -> bytes:
    f = Fernet(key) # create a Fernet object using the provided key
    encoded_message = message.encode('utf-8') # python stings must be converted the can be encryoted."utf-8" it converts the string to bytes using the standard utf-8 format
    encrypted_data = f.encrypt(encoded_message) # calls the fernet object's 'encrypt' methods.this process encrypts the data and adds a messagge authentication code(MAC) for tamper proofing(to detect any unauthorized modifications to the data)
    return encrypted_data

def decrypt_message(encrypted_data: bytes, key: bytes) -> str: # defines the decryption funtion. it takes encrypted bytes and bytes key and returns the original plain text in string.
    f = Fernet(key) # create a new fernet object, intialized with the key(must be the exact same key used for encryption)
    decrypted_data = f.decrypt(encrypted_data) # it calls the fernet object's "decrypt" method.this is a critical step that also verifies the MAC.if the key is wrong or the data was tampered with,this line will rise an "invalid exception" error
    decoded_message = decrypted_data.decode('utf-8') # it converts the decrypted bytes back into a readable python string using "utf-8"
    return decoded_message
"""
Explanation from(Line No-57 to Line No-82):-
This block checks if the script is being run directly (as opposed to being imported as a module). If so, it executes the key setup process. 
It first attempts to load an existing encryption key from a file or generates a new one if the file does not exist. 
The active key is then printed in a human-readable format (decoded from bytes to a UTF-8 string) for the user's reference.
"""
if __name__ == "__main__": # this standard python guard ensures the code inside only runs when the script is executed directly(not when imported as module)
    print("1.Key Setup")
    encryption_key = load_or_generate_key()
    print(f"Active Key: {encryption_key.decode('utf-8')}")
    print("2.Get User Input")
    original_message = input("Please enter the words, sentence, or number you want to encrypt: ")
    print(f"Original Message: {original_message}")
    print("3.Encryption Process")
    try:
        encrypted_msg = encrypt_message(original_message, encryption_key)
        print(f"Encrypted Data (string representation): {encrypted_msg.decode('utf-8')}")
    except Exception as e:
        print(f"Encryption failed: {e}")
        exit()
    print("4. Decryption Process")
    try:
        decrypted_msg = decrypt_message(encrypted_msg, encryption_key)
        print(f"Decrypted Message: {decrypted_msg}")
    except Exception as e:
        print(f"Decryption failed (Key might be wrong or data tampered with): {e}")
        decrypted_msg = None
    print("5. Verification")
    if original_message == decrypted_msg:
        print("Success: Original message matches decrypted message! ")
    else:
        print("Failure: Decryption result does not match original message.")