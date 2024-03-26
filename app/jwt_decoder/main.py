import jwt

# Specify the path to your JWT file
jwt_file_path = './token.txt'
output_file_path='./decoded_token.txt'

with open(jwt_file_path, 'r') as file:
    token = file.read().strip()  # Ensure to strip any whitespace/newlines
            

# Secret or public key used to encode the JWT. 
# This is only necessary if the JWT is encoded with a secret or key.
# For demonstration, we're skipping signature verification.
# secret_key = "your_secret_key"

try:
    # Decode the JWT without verifying the signature.
    # WARNING: This should only be used for debugging or in contexts where
    # you trust the source of the JWT. It's insecure to skip verification in production.
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    # Write the decoded JWT to a txt file
    with open(output_file_path, 'w') as file:
        # Convert the decoded dictionary to a string before writing to file
        file.write(str(decoded))
    
    print(f"Decoded JWT written to {output_file_path}")
except jwt.PyJWTError as e:
    # Handle decoding errors (e.g., invalid token format)
    print(f"JWT decoding error: {e}")

