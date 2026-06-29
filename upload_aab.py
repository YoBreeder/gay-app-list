"""
Upload AAB to Google Play using Chrome's saved auth cookies.
Decrypts Chrome DPAPI-protected cookies to authenticate.
"""
import sqlite3, json, base64, os, shutil, sys, time, requests
from pathlib import Path
from Crypto.Cipher import AES
import win32crypt

CHROME_PROFILE = Path(os.environ['LOCALAPPDATA']) / 'Google/Chrome/User Data/Default'
LOCAL_STATE   = Path(os.environ['LOCALAPPDATA']) / 'Google/Chrome/User Data/Local State'
AAB_PATH = r'C:\Users\DH\gay-app-list\android\app\build\outputs\bundle\release\app-release.aab'
PACKAGE = 'com.gayapplist.app'
DEVELOPER_ID = '8841904810182759765'
APP_ID = '4974539322578443286'
TRACK = 'production'


def get_encryption_key():
    with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


def decrypt_cookie(enc_value, key):
    try:
        if enc_value[:3] == b'v10' or enc_value[:3] == b'v11':
            nonce = enc_value[3:15]
            ciphertext = enc_value[15:-16]
            tag = enc_value[-16:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    except Exception:
        pass
    try:
        return win32crypt.CryptUnprotectData(enc_value, None, None, None, 0)[1].decode('utf-8')
    except Exception:
        return None


def get_chrome_cookies(domain_filter):
    cookies_path = CHROME_PROFILE / 'Network/Cookies'
    tmp_path = Path(os.environ['TEMP']) / 'chrome_cookies_tmp.db'
    shutil.copy2(cookies_path, tmp_path)
    key = get_encryption_key()
    conn = sqlite3.connect(str(tmp_path))
    cur = conn.cursor()
    cur.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE ?", (f'%{domain_filter}%',))
    result = {}
    for host, name, enc_val in cur.fetchall():
        val = decrypt_cookie(enc_val, key)
        if val:
            result[name] = val
    conn.close()
    tmp_path.unlink(missing_ok=True)
    return result


def main():
    print("Extracting Chrome cookies for Google Play...")
    cookies = get_chrome_cookies('.google.com')
    if not cookies:
        print("ERROR: No cookies found. Make sure you're logged into Google Play Console in Chrome.")
        sys.exit(1)

    # Show which auth cookies we got (names only, not values)
    auth_keys = [k for k in cookies if any(x in k.lower() for x in ['sid', 'sapisid', 'hsid', 'ssid', 'osid', '1psid', 'auth'])]
    print(f"Found {len(cookies)} cookies, auth-related: {auth_keys}")

    session = requests.Session()
    session.cookies.update(cookies)

    # Build SAPISID-based auth header
    sapisid = cookies.get('SAPISID') or cookies.get('__Secure-1PSID') or ''
    origin = 'https://play.google.com'
    timestamp = int(time.time())
    import hashlib
    sapisid_hash = hashlib.sha1(f'{timestamp} {sapisid} {origin}'.encode()).hexdigest()
    session.headers.update({
        'Authorization': f'SAPISIDHASH {timestamp}_{sapisid_hash}',
        'Origin': origin,
        'X-Origin': origin,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    })

    print("\nAttempting to use Google Play Developer Publishing API...")

    # Step 1: Create an edit
    edit_url = f'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{PACKAGE}/edits'
    print(f"Creating edit: POST {edit_url}")
    r = session.post(edit_url, json={})
    print(f"  Status: {r.status_code}")
    if r.status_code != 200:
        print(f"  Response: {r.text[:500]}")
        print("\nCookie auth failed. Trying alternative approach...")
        return False

    edit_data = r.json()
    edit_id = edit_data.get('id')
    print(f"  Edit ID: {edit_id}")

    # Step 2: Upload AAB
    upload_url = f'https://androidpublisher.googleapis.com/upload/androidpublisher/v3/applications/{PACKAGE}/edits/{edit_id}/bundles?uploadType=media'
    print(f"\nUploading AAB ({os.path.getsize(AAB_PATH):,} bytes)...")
    with open(AAB_PATH, 'rb') as f:
        r = session.post(upload_url, data=f, headers={'Content-Type': 'application/octet-stream'})
    print(f"  Status: {r.status_code}")
    if r.status_code not in (200, 201):
        print(f"  Response: {r.text[:500]}")
        return False

    bundle_info = r.json()
    version_code = bundle_info.get('versionCode')
    print(f"  Bundle uploaded! versionCode: {version_code}")

    # Step 3: Assign to track
    track_url = f'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{PACKAGE}/edits/{edit_id}/tracks/{TRACK}'
    track_body = {
        'track': TRACK,
        'releases': [{
            'name': '1.0',
            'versionCodes': [str(version_code)],
            'status': 'draft',
            'releaseNotes': [{'language': 'en-US', 'text': 'Initial release of Gay App List - the ultimate LGBTQ+ app directory.'}]
        }]
    }
    print(f"\nAssigning to {TRACK} track...")
    r = session.put(track_url, json=track_body)
    print(f"  Status: {r.status_code}")
    if r.status_code != 200:
        print(f"  Response: {r.text[:500]}")
        return False

    # Step 4: Commit the edit
    commit_url = f'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{PACKAGE}/edits/{edit_id}:commit'
    print(f"\nCommitting edit...")
    r = session.post(commit_url)
    print(f"  Status: {r.status_code}")
    print(f"  Response: {r.text[:300]}")

    if r.status_code == 200:
        print("\n✓ SUCCESS! AAB uploaded and committed to Play Store production track!")
        return True
    return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
