import struct, os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

def decrypt_file(key, in_file):
    out_file = in_file.replace('.locked', '')
    with open(in_file, 'rb') as infile, open(out_file, 'wb') as outfile:
        filesize = struct.unpack('<Q', infile.read(8))[0]
        iv = infile.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        while True:
            chunk = infile.read(128 * 1024)
            if not chunk:
                break
            outfile.write(cipher.decrypt(chunk))
        outfile.truncate(filesize)

def load_key():
    with open("private.pem", "rb") as f:
        private_key = RSA.import_key(f.read())
    with open("KEY-README.txt", "rb") as f:
        lines = f.readlines()
        enc_key = b''.join(lines[3:])
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(enc_key)

def main():
    key = load_key()
    for root, dirs, files in os.walk("C:/"):
        for file in files:
            if file.endswith(".locked"):
                try:
                    decrypt_file(key, os.path.join(root, file))
                    os.remove(os.path.join(root, file))
                except:
                    pass

if __name__ == "__main__":
    main()
