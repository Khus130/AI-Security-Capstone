import json
import time
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

# ==============================
# AUTH0 CONFIGURATION
# ==============================

DOMAIN = "dev-udhy0pqmtyquxcff.us.auth0.com"

CLIENT_ID = "3uGJyhEtlOdqm8Wz18tECZX8oGvx25Im"
CLIENT_SECRET = "aJ_ml83mLoYeb13pZmIsCKl-IQNcSsJgVtqhPU1ExCI6_7fwt7v3eF5y-1aqdOGC"

AUDIENCE = "https://ai-agent-api"
CALLBACK = "http://localhost:3000/callback"

# ==============================
# CALLBACK SERVER
# ==============================

authorization_code = None


class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global authorization_code

        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            authorization_code = params["code"][0]

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.wfile.write(
                b"<h2>Authorization successful.</h2>"
                b"<p>You can close this browser window.</p>"
            )
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed.")

    def log_message(self, format, *args):
        pass


# ==============================
# AUTHORIZATION
# ==============================

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": CALLBACK,
    "scope": "openid profile email offline_access",
    "audience": AUDIENCE,
    "prompt": "login"
}

auth_url = (
    f"https://{DOMAIN}/authorize?"
    + urllib.parse.urlencode(params)
)

print("=" * 65)
print("PROJECT 4 - REFRESH TOKEN ROTATION TEST")
print("=" * 65)

print("\n[1] Opening Auth0 Universal Login...")
print("[INFO] Complete login in the browser.")

server = HTTPServer(("localhost", 3000), CallbackHandler)
server.timeout = 120

webbrowser.open(auth_url)

while authorization_code is None:
    server.handle_request()

server.server_close()

print("[SUCCESS] Authorization code received.")

# ==============================
# CODE → TOKENS
# ==============================

token_url = f"https://{DOMAIN}/oauth/token"

token_data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": authorization_code,
    "redirect_uri": CALLBACK
}

request = urllib.request.Request(
    token_url,
    data=urllib.parse.urlencode(token_data).encode(),
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    method="POST"
)

with urllib.request.urlopen(request) as response:
    token_response = json.loads(response.read().decode())

refresh_token_1 = token_response["refresh_token"]

print("\n[2] INITIAL TOKEN RESPONSE")
print("[SUCCESS] Refresh Token 1 obtained.")

# ==============================
# USE RT1 → GET RT2
# ==============================

print("\n[3] USING REFRESH TOKEN 1...")
print("[INFO] Exchanging RT1 for a new refresh token.")

refresh_data = {
    "grant_type": "refresh_token",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": refresh_token_1
}

request = urllib.request.Request(
    token_url,
    data=urllib.parse.urlencode(refresh_data).encode(),
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    method="POST"
)

with urllib.request.urlopen(request) as response:
    first_refresh_response = json.loads(response.read().decode())

refresh_token_2 = first_refresh_response["refresh_token"]

print("[SUCCESS] RT1 accepted.")
print("[SUCCESS] New Refresh Token 2 issued.")
print("[INFO] Old Refresh Token 1 should now be invalid.")

# ==============================
# REPLAY OLD RT1
# ==============================

print("\n[4] REPLAYING OLD REFRESH TOKEN 1...")
print("[INFO] Sending the already-used RT1 to Auth0 again...")

time.sleep(1)

replay_data = {
    "grant_type": "refresh_token",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": refresh_token_1
}

request = urllib.request.Request(
    token_url,
    data=urllib.parse.urlencode(replay_data).encode(),
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    method="POST"
)

try:
    urllib.request.urlopen(request)

    print("\n[WARNING] OLD REFRESH TOKEN WAS ACCEPTED.")
    print("[WARNING] Rotation/reuse protection did not reject the replay.")

except urllib.error.HTTPError as error:

    error_body = error.read().decode()

    print("\n" + "=" * 65)
    print("EXPECTED REJECTION")
    print("=" * 65)
    print("[BLOCKED] Old refresh token replay was rejected by Auth0.")
    print(f"[HTTP STATUS] {error.code}")
    print("[AUTH0 ERROR RESPONSE]")
    print(error_body)
    print("=" * 65)
