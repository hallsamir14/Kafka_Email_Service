import jwt
def readUser(sampleToken_path:str):
    #Specify the path to your JWT file
    decoded_token = None
    with open(sampleToken_path, 'r') as file:
        token = file.read().strip()  # Ensure to strip any whitespace/newlines
        
        # Secret or public key used to encode the JWT. 
        # This is only necessary if the JWT is encoded with a secret or key.
        # For demonstration, we're skipping signature verification.
        # secret_key = "your_secret_key"

        # Decode the JWT without verifying the signature.
        # WARNING: This should only be used for debugging or in contexts where
        # you trust the source of the JWT. It's insecure to skip verification in production.
        decoded_token = jwt.decode(token, options={"verify_signature": False})
    
    # Write the decoded JWT to a txt file
    return {"token": decoded_token}   

def main():
    # print(readUser('./token.txt'))
    # Extract email and email verification status from the decoded JWT
    print(readUser('./token.txt')['token']['email'])
    print(readUser('./token.txt')['token']['email_verified'])
if __name__ == "__main__":
    main()

