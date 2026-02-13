# How to Review PRs with GitHub Copilot 🕵️‍♂️🤖

So you've raised a PR (or want to review one) and want Copilot's help?
Here is the pro workflow.

## 1. The Setup (One-Time)

You need **two** extensions in VS Code:
1.  **GitHub Copilot** (You already have this).
2.  **GitHub Pull Requests and Issues** (Install this now).

## 2. Open the PR in VS Code

1.  Click the **GitHub icon** in the sidebar (cat icon).
2.  Under **Pull Requests**, find your PR.
3.  Right-click the PR description -> **Checkout**.
    *   *This downloads the PR code to your local machine.*

## 3. Review with Copilot

Now that the code is local, use Copilot to review it:

### Method A: The "Explain" Review
1.  Open a file changed in the PR.
2.  Select the new code.
3.  Press **Ctrl+I** (Inline Chat).
4.  Type:
    > "Review this change. Are there any bugs or security issues?"

### Method B: The "Diff" Review
1.  Open the **Source Control** tab (Git icon).
2.  Click a file to see the **Diff** (changes).
3.  Copilot can analyze the *added* lines (green). Highlight them and ask:
    > "Is this implementation efficient?"

## 4. Applying Fixes

If Copilot finds a bug:
1.  Click **Accept** on its suggestion.
2.  Commit the fix: `git commit -m "fix: copilot review suggestions"`.
3.  Push: `git push`.
    *   *This updates the PR automatically on GitHub!*
