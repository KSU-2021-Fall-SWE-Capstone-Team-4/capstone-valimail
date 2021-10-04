from dane_jwe_jws.authentication import Authentication

test_message = "hello yeye!!"
prikey_path = 'prikey.txt'
identity_name = "2fcf9ecce81b47d8b7884a7c158ea4a2.s1.eu.hivemq.cloud"
signed = Authentication.sign(test_message, prikey_path, identity_name)
print(signed)

validated = Authentication.verify(signed)
print(validated)
