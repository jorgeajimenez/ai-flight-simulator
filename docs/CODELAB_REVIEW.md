# Codelab Forensic Review & Recommended Fixes

## 🖼️ Why the Images are "Not Loading"
The placeholder images generated earlier are **1x1 pixel transparent PNGs**. GitHub attempts to render them, but because they are transparent and 1 pixel wide, they appear as invisible, broken, or blurry boxes. **This is expected behavior.** Once you replace these `assets/*.png` files with your actual screenshots during the dry run, they will render perfectly.

---

## 🃏 Why the Mocking/Secrets Section is Confusing
The Codelab introduces **Test-Driven Development (TDD)** and `pytest-mock` in Module 2 to explain how we avoid hitting the real Secret Manager API during tests. However, the codelab *never instructs the user to actually run the tests*. It throws abstract theory at the user without any hands-on practice, causing unnecessary cognitive load.

---

## 🔍 "Fine-Tooth Comb" Deficiencies (Action Required)

If an attendee runs this codelab right now with a fresh Gmail account, they will hit several hard blockers. Here are the issues that need to be addressed before sharing:

### 1. CRITICAL BLOCKER: The `uv` CLI is Missing in Cloud Shell
*   **The Problem:** Module 1 instructs the user to run `uv sync` immediately after cloning the repo. **Google Cloud Shell does not have `uv` installed by default.** The command will fail immediately with `command not found: uv`.
*   **Recommended Fix:** Add the `uv` installation command (`curl -LsSf https://astral.sh/uv/install.sh | sh`) to the setup instructions in Module 1, or add it directly to the `scripts/setup_gcp.sh` script so it installs automatically.

### 2. The TDD/Mocking Disconnect (Module 2)
*   **The Problem:** As mentioned above, showing a mocked test without having the user run it is confusing.
*   **Recommended Fix:** We must either give them the command to run it (e.g., `uv run pytest tests/test_vault.py`) so they experience the "Red -> Green" workflow, OR we should delete the TDD section entirely and focus purely on building the services.

### 3. Inconsistent "Action" Steps (Modules 3, 5, 6)
*   **The Problem:** Module 2 is great because it explicitly says "Open `app.py`, find this marker, and paste this code." However, Modules 3, 5, and 6 just show the architecture and explain the code without ever telling the user *what to do with it*. The user will reach the end of the page and think, "Okay... was I supposed to copy that somewhere?"
*   **Recommended Fix:** Every module needs explicit, bold instructions like: *"Open `services/geospatial.py`, locate `[CODELAB STEP 2A]`, and paste the following code."*

### 4. The Gemini CLI Ambiguity (Module 4)
*   **The Problem:** Module 4 says, *"You will use the Gemini CLI to implement the following within `analyze_and_terraform`"*. However, it doesn't give the user the prompt to use, nor does it provide the exact code to copy-paste if the CLI fails them or if they get stuck.
*   **Recommended Fix:** We need to provide the exact code blocks to copy-paste, just like the other modules, to ensure a seamless workshop experience for everyone, regardless of whether the AI generates the perfect code on the first try.