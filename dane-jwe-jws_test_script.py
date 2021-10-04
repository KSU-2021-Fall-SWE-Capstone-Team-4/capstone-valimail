from dane_jwe_jws.authentication import Authentication

test_message = "hello yeye!!"
prikey_path = 'prikey.txt'
identity_name = "google.com"
signed = Authentication.sign(test_message, prikey_path, identity_name)
print(signed)

validated = Authentication.verify(signed)
print(validated)
