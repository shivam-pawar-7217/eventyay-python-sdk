# GitHub Copilot Setup & Usage Guide 🤖

Congratulations on activating your GitHub Student Pack!
Here is how to leverage **Copilot** to review your code and speed up development.

## 1. Installation (VS Code)

1.  Open VS Code.
2.  Go to **Extensions** (Ctrl+Shift+X).
3.  Search for **"GitHub Copilot"**.
4.  Click **Install**.
5.  (Optional) Install **"GitHub Copilot Chat"** for the sidebar chat interface.

## 2. Authentication

1.  After installation, a prompt will appear in the bottom-right corner.
2.  Click **"Sign in to GitHub"**.
3.  Authorize VS Code in your browser.
4.  Once signed in, you should see a small Copilot icon in the status bar (bottom right).

## 3. How to Review Code

### Method A: Copilot Chat (Best for "Review")
1.  Open the file you want to review (e.g., `eventyay/client.py`).
2.  Open the **Chat Panel** (Ctrl+Alt+I or click the Chat icon in the sidebar).
3.  Type:
    > "Review this file for potential bugs, security issues, and improvements. Explain like I'm a beginner."
4.  Copilot will analyze the open file and give you a structured review.

## FAQ: Can I review PRs on standard GitHub.com?

**No.** The direct "Review PR" button on the GitHub website is an **Enterprise feature**.
As a student (Copilot Individual), you must use the **VS Code** method:
1.  Check out the PR locally.
2.  Use Copilot Chat in VS Code to review changes.

### Method B: Inline Chat
1.  Highlight a block of code.
2.  Press **Ctrl+I** (Cmd+I on Mac).
3.  Type: *"Refactor this to be more robust"* or *"Explain this code"*.
4.  Copilot will suggest changes directly in the editor.

## 4. GSoC Strategy using Copilot

Use Copilot to help draft your proposal:
*   **Explain Code**: "Explain the `OrganizersMixin` logic for my proposal technical section."
*   **Generate Tests**: "Write unit tests for this function covering edge cases."
*   **Brainstorm**: "What other features should an Event API SDK have?"

---
**Status**: Ready to use! 🚀
