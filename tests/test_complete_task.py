import os
import time
import tempfile
from playwright.sync_api import sync_playwright, expect

def test_complete_task():
    # Create a temporary version of index.html without external fonts to avoid timeouts
    with open("index.html", "r") as f:
        content = f.read()

    # Remove external font links that cause timeouts in the sandbox
    content = content.replace("https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap", "")

    # Use tempfile.NamedTemporaryFile to safely create temp file in system temp dir
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False) as tf:
        tf.write(content)
        temp_filepath = tf.name

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Open the file via file:// protocol directly
            page.goto(f"file://{temp_filepath}", wait_until="load")

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

            # Trigger openModal(1) to set currentTask
            page.evaluate("openModal(1)")

            # Trigger completeTask()
            page.evaluate("completeTask()")

            # Verify task element has 'done' class
            task_el = page.locator("#task-1")
            expect(task_el).to_have_class("task-item done")

            # Verify check element text is '✓'
            check_el = page.locator("#check-1")
            expect(check_el).to_have_text("✓")

            # Verify completedTasks Set contains 1
            has_completed = page.evaluate("completedTasks.has(1)")
            assert has_completed is True, "completedTasks should contain 1"

            # Verify progress update (assuming TOTAL is 2 based on count / TOTAL logic)
            total_tasks = page.evaluate("TOTAL")
            progress_count = page.locator("#progress-count")
            expect(progress_count).to_have_text(f"1 / {total_tasks} tarefas")

            # Check modal closed (closeModal was called)
            overlay = page.locator("#modal-overlay")
            expect(overlay).to_have_class("modal-overlay")

            # Verify currentTask is null
            current_task = page.evaluate("currentTask")
            assert current_task is None, f"Expected currentTask to be null, got {current_task}"

            print("Test passed successfully!")
            browser.close()
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

if __name__ == "__main__":
    test_complete_task()
