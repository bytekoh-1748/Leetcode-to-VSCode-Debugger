# Changelog

All notable changes to this project will be documented in this file.

## 0.1.1

- Added fallback helper-type inference for untyped LeetCode parameters like `root` and `head`.
- Improved runtime compatibility for pasted solutions where `TreeNode` and `ListNode` annotations were removed.

## 0.1.0

- Added support for `Solution` helper methods such as `dfs` and `helper` without breaking method inference.
- Improved case-file parsing so named `Input:` blocks still work when method parameter names differ from LeetCode's defaults.
- Added marketplace metadata, packaging scripts, and release assets for VS Code Marketplace publishing.

## 0.0.1

- Initial local extension release for debugging LeetCode Python solutions in VS Code.
