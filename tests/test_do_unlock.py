import os
import time
import tempfile
import urllib.parse
import urllib.request
from playwright.sync_api import sync_playwright, expect

def test_do_unlock():
    # Resolve absolute path to index.html to be resilient against the working directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(base_dir, "index.html")

    # Create a temporary version of index.html without external fonts to avoid timeouts
    with open(index_path, "r") as f:
        content = f.read()

    # Remove external font links that cause timeouts in the sandbox
    content = content.replace("https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap", "")

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False) as tf:
        tf.write(content)
        temp_filepath = tf.name

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Use file protocol to serve the temporary file without http server
            file_url = urllib.parse.urljoin('file:', urllib.request.pathname2url(os.path.abspath(temp_filepath)))
            page.goto(file_url, wait_until="load")

            # Wait for doUnlock to be defined
            for _ in range(100):
                try:
                    is_defined = page.evaluate("typeof doUnlock !== 'undefined'")
                    if is_defined:
                        break
                except Exception:
                    pass
                time.sleep(0.1)
            else:
                raise RuntimeError("doUnlock was not defined in time")

            # Test Early Return (not enough tasks completed)
            # Call doUnlock()
            page.evaluate("doUnlock()")

            # Verify nothing changed
            lock_box_display = page.evaluate("document.getElementById('lock-box').style.display")
            assert lock_box_display != "none", f"Expected lock-box display not to be 'none', but got {lock_box_display}"

            unlocked_area = page.locator("#unlocked-area")
            expect(unlocked_area).not_to_have_class("unlocked-content show")

            # Test Happy Path (all tasks completed)
            # Add TOTAL tasks to completedTasks dynamically so it won't break if TOTAL changes
            page.evaluate("for (let i = 1; i <= TOTAL; i++) { completedTasks.add(i); }")

            # Mock scrollIntoView to prevent errors during testing since Playwright might have issues with smooth scroll in headless if not handled or it's fine but we can stub it just in case. It's actually fine natively.
            page.evaluate("document.getElementById('unlocked-area').scrollIntoView = function() {};")

            # Call doUnlock() again
            page.evaluate("doUnlock()")

            # Assertions
            # 1. lock-box display is 'none'
            lock_box_display = page.evaluate("document.getElementById('lock-box').style.display")
            assert lock_box_display == "none", f"Expected lock-box display to be 'none', but got {lock_box_display}"

            # 2. content-text style filter is 'none'
            content_text_filter = page.evaluate("document.querySelector('#preview-area .content-text').style.filter")
            assert content_text_filter == "none", f"Expected content-text filter to be 'none', but got {content_text_filter}"

            # 3. blur-overlay display is 'none'
            blur_overlay_display = page.evaluate("document.querySelector('#preview-area .blur-overlay').style.display")
            assert blur_overlay_display == "none", f"Expected blur-overlay display to be 'none', but got {blur_overlay_display}"

            # 4. tag text content is '✅ Desbloqueado'
            tag_text = page.evaluate("document.querySelector('#preview-area .tag').textContent")
            assert tag_text == "✅ Desbloqueado", f"Expected tag text to be '✅ Desbloqueado', but got {tag_text}"

            # 5. unlockedArea has 'show' class
            expect(unlocked_area).to_have_class("unlocked-content show")

            print("Test passed successfully!")
            browser.close()
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

if __name__ == "__main__":
    test_do_unlock()
