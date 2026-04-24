from __future__ import annotations

import socket
import sys
import webbrowser

from automation.app import create_app


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def main() -> None:
    host = "127.0.0.1"
    port = 8010
    app_url = f"http://{host}:{port}/health"

    if is_port_in_use(port, host):
        print(f"[INFO] Port {port} is already in use.")
        print(f"[INFO] Open app manually: {app_url}")
        input("Press Enter to exit...")
        return

    print("[INFO] Starting Egypt SMB Automation API (Fixed)...")
    print(f"[INFO] Health URL: {app_url}")
    print("[INFO] Keep this window open while using the API.")

    try:
        webbrowser.open(app_url)
    except Exception:
        pass

    try:
        app = create_app()
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"[ERROR] Failed to start server: {exc}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()

