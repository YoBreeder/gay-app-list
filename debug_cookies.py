import sqlite3, shutil, os, json, base64
from pathlib import Path
import win32crypt
from Crypto.Cipher import AES

CHROME_PROFILE = Path(os.environ['LOCALAPPDATA']) / 'Google/Chrome/User Data/Default'
LOCAL_STATE = Path(os.environ['LOCALAPPDATA']) / 'Google/Chrome/User Data/Local State'

cookies_path = CHROME_PROFILE / 'Network/Cookies'
tmp = Path(os.environ['TEMP']) / 'ck_debug2.db'
shutil.copy2(cookies_path, tmp)
conn = sqlite3.connect(str(tmp))
cur = conn.cursor()
cur.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%google.com%' ORDER BY host_key, name")
rows = cur.fetchall()
conn.close()
tmp.unlink()

print(f"Total google cookies: {len(rows)}")
for host, name, enc in rows[:50]:
    print(f"  {host}: {name} (enc_len={len(enc)})")

# Try decrypt one
with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
    local_state = json.load(f)
encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
print(f"\nDecryption key obtained: {len(key)} bytes")

# Try decrypting first encrypted cookie
for host, name, enc_val in rows:
    if enc_val and len(enc_val) > 3:
        try:
            if enc_val[:3] in (b'v10', b'v11'):
                nonce = enc_val[3:15]
                ciphertext = enc_val[15:-16]
                tag = enc_val[-16:]
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                val = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
                print(f"Sample decrypt OK: {host} / {name} = {val[:30]}...")
                break
        except Exception as e:
            print(f"Decrypt failed for {host}/{name}: {e}")
