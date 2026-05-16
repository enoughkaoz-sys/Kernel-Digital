import os
import time
import tempfile
import subprocess
import signal
from playwright.sync_api import sync_playwright, expect

def test_close_modal():
    # Start http server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Intercept and abort external font requests to avoid timeouts in the sandbox
            page.route("**/*", lambda route: route.abort() if "fonts.googleapis.com" in route.request.url or "fonts.gstatic.com" in route.request.url else route.continue_())

            # Use http server to serve the local index.html
            page.goto("http://localhost:8001/index.html", wait_until="load")

            # Wait for openModal to be defined
            for _ in range(100):
                try:
                    is_defined = page.evaluate("typeof openModal !== 'undefined'")
                    if is_defined:
                        break
                except Exception:
                    pass
                time.sleep(0.1)
            else:
                raise RuntimeError("openModal was not defined in time")

            # Trigger openModal(1)
            page.evaluate("openModal(1)")

            # Verify the #modal-overlay element has the 'show' class
            overlay = page.locator("#modal-overlay")
            expect(overlay).to_have_class("modal-overlay show")

            # Verify currentTask is 1
            current_task = page.evaluate("currentTask")
            assert current_task == 1, f"Expected currentTask to be 1, but got {current_task}"

            # Click the "Cancelar" button to trigger closeModal()
            cancel_button = page.locator(".btn-modal-cancel")
            cancel_button.click()

            # Verify the #modal-overlay element no longer has the 'show' class
            expect(overlay).to_have_class("modal-overlay")

            # Verify that the JavaScript variable currentTask is null
            current_task_after = page.evaluate("currentTask")
            assert current_task_after is None, f"Expected currentTask to be None, but got {current_task_after}"

            print("Test passed successfully!")
            browser.close()
    finally:
        os.kill(server_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_close_modal()
