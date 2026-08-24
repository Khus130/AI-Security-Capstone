from datetime import datetime
import time


def anomaly_token_reuse_detection():

    print("\n" + "=" * 70)
    print("PROJECT 4 - ANOMALY DETECTION TEST")
    print("=" * 70)

    # Simulated token information
    token_id = "RT-DEMO-001"
    identity = "agent-user-01"

    # Token expires immediately for demonstration
    issued_time = time.time()
    expiry_time = issued_time + 2

    print(f"\n[IDENTITY] {identity}")
    print(f"[TOKEN] {token_id}")
    print("[EVENT] Refresh token issued")

    # Wait until token expires
    print("\n[INFO] Waiting for token to expire...")
    time.sleep(3)

    current_time = time.time()

    print("\n[EVENT] Attempting to reuse expired token")

    # Detection condition
    if current_time > expiry_time:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        print("\n" + "-" * 70)
        print("[ANOMALY DETECTED]")
        print(f"[TIMESTAMP] {timestamp}")
        print(f"[IDENTITY] {identity}")
        print("[EVENT TYPE] TOKEN_REUSE_AFTER_EXPIRY")
        print("[REASON] Expired refresh token was reused")
        print("[ACTION] Request blocked")
        print("[STATUS] SECURITY ALERT FIRED")
        print("-" * 70)

    else:
        print("[STATUS] No anomaly detected")

    print("=" * 70)


if __name__ == "__main__":
    anomaly_token_reuse_detection()
