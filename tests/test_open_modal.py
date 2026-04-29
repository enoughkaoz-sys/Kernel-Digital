import os
import time
import tempfile
import subprocess
import signal
from playwright.sync_api import sync_playwright, expect

def test_open_modal():
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

                # Verify initial state
                current_task = page.evaluate("currentTask")
                assert current_task is None, f"Expected currentTask to be None initially, but got {current_task}"

                overlay = page.locator("#modal-overlay")
                expect(overlay).not_to_have_class("modal-overlay show")

                # Test Happy Path: openModal(1)
                page.evaluate("openModal(1)")

                # Verify currentTask is updated
                current_task = page.evaluate("currentTask")
                assert current_task == 1, f"Expected currentTask to be 1, but got {current_task}"

                # Verify overlay has show class
                expect(overlay).to_have_class("modal-overlay show")

                # Verify DOM content from tasks[1]
                # tasks[1]: icon='🎵', title='Baixar TikTok ou Kwai', desc='Instale o app de vídeos parceiro pelo link abaixo e assista alguns minutos para confirmar.'
                icon_text = page.locator("#modal-icon").text_content()
                assert icon_text == "🎵", f"Expected modal icon '🎵', got '{icon_text}'"

                title_text = page.locator("#modal-title").text_content()
                assert title_text == "Baixar TikTok ou Kwai", f"Expected title 'Baixar TikTok ou Kwai', got '{title_text}'"

                desc_text = page.locator("#modal-desc").text_content()
                assert desc_text == "Instale o app de vídeos parceiro pelo link abaixo e assista alguns minutos para confirmar.", f"Expected desc, got '{desc_text}'"

                steps_count = page.locator("#modal-steps li").count()
                assert steps_count == 4, f"Expected 4 steps, got {steps_count}"


                # Close the modal to reset state
                page.evaluate("closeModal()")
                expect(overlay).not_to_have_class("modal-overlay show")

                # Test Completed Task Path: openModal(2) after completedTasks.add(2)
                page.evaluate("completedTasks.add(2)")
                page.evaluate("openModal(2)")

                # Verify currentTask is not updated to 2 (should be null since we closed the previous one, but definitely not 2)
                current_task = page.evaluate("currentTask")
                assert current_task is None, f"Expected currentTask to be None (since task 2 is already completed), but got {current_task}"

                # Verify overlay does NOT have show class
                expect(overlay).not_to_have_class("modal-overlay show")

                print("Test passed successfully!")
                browser.close()
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    finally:
        os.kill(server_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_open_modal()
