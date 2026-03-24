# Changelog

All notable changes to this project will be documented in this file.

## 0.1.6

- Added a per-case timeout that stops suspected infinite loops and reports them in the debug output.
- Documented the infinite-loop timeout behavior and configuration in the README.

## 0.1.5

- Added Python 3.x compatibility fallbacks for runtime imports used by the VS Code debugger.
- Documented that the extension runs on Python 3.9 or newer.
- Added a clear startup error when the selected VS Code Python interpreter is older than Python 3.9.

## 0.1.4

- Added support for multiline named `Input:` values such as `grid = [...]` in case files.


## 0.1.3

- Updated the Marketplace demo video link and refreshed the release package.

## 0.1.2

- Rewrote the README for Marketplace users so installation and usage steps match the published extension workflow.

## 0.1.1

- Added fallback helper-type inference for untyped LeetCode parameters like `root` and `head`.
- Improved runtime compatibility for pasted solutions where `TreeNode` and `ListNode` annotations were removed.

## 0.1.0

- Added support for `Solution` helper methods such as `dfs` and `helper` without breaking method inference.
- Improved case-file parsing so named `Input:` blocks still work when method parameter names differ from LeetCode's defaults.
- Added marketplace metadata, packaging scripts, and release assets for VS Code Marketplace publishing.

## 0.0.1

- Initial local extension release for debugging LeetCode Python solutions in VS Code.
