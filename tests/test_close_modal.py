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
        # Create a temporary version of index.html without external fonts to avoid timeouts
        with open("index.html", "r") as f:
            content = f.read()

        # Remove external font links that cause timeouts in the sandbox
        content = content.replace("https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap", "")

        with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False, dir=os.getcwd()) as tf:
            tf.write(content)
            temp_filename = os.path.basename(tf.name)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # Use http server to serve the temporary file
                page.goto(f"http://localhost:8001/{temp_filename}", wait_until="load")

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
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    finally:
        os.kill(server_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_close_modal()
