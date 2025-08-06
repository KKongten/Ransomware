# Ransomware Source Code 

## Using Language
 - Python 3.7.4 → 3.13.5 
 - Window Batch File 

---
*This project is **strictly for educational and research purposes***. <br>
*Executing this code on any production system, personal computer, or network is **strongly discouraged and may result in permanent data loss***.
---
## Code Update ( 25.08.06 )
### 1. AES Key Management
 - Replaced static AES key with **randomly generated AES-256 key**
 - Each AES key is encrypted using **RSA public key** (`public.pem`)
 - Encrypted key is stored in `KEY-README.txt` for manual decryption testing

### 2. Target Extension
 - Previous version : Encrypts only files inside a specific folder. 
 - Update Version : Scans **all available drives (C:\ ~ Z:\)** and targets files by extension (`.docx`, `.pdf`, `.jpg`, etc.)

### 3. Anti-Recovery Techniques
 - Deletes **shadow copies** using `vssadmin`
 - Prepares for **stealth improvements** (not yet fully implemented):
   - Event log deletion
   - Process hiding
   - Background execution
 
### 4. Persistence
 - Adds itself to **Startup folder via Windows registry** (`HKCU\...\Run`)
 - Automatically re-executes upon reboot

### 5. GUI Removed
 - GUI interface replace with **direct execuion behavior**
 - Automatically encrypts upon running in VM environment. 

---

## How to Use (For Researchers)

### 1. Setup RSA Keys
```commandline
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

### 2. Run inside a VM (Never on Host)
```commandline
python ransomware.py
```

### 3. To Decrypt (Using decrypt_tool.py)
 - Place private.pem and KEY-README.txt in the same folder.
 - Run python decrypt_tool.py

## Legal Disclaimer
***This repository is intended for academic study and malware behavior analysis only.***<br>
***Any misuse of the code is the sole responsibility of the executor.***<br>
***The author is not liable for any damage caused by misuse.***