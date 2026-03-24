# LeetCode Debugger

Debug the active LeetCode Python solution in VS Code with a same-name `.txt` case file.

Use it to paste LeetCode Python solutions into VS Code, open a matching case file, set breakpoints, and debug with the normal Python debugger.

## Demo

- [YouTube demo video](https://youtu.be/6nRcja5qnYQ?si=fq9mFnLnVvhRpKbY)

## Install

1. Install `LeetCode Debugger` from the VS Code Marketplace.
2. Make sure the VS Code `Python` and `Python Debugger` extensions are installed.
3. Open the folder where your LeetCode Python files live.

## Features

- Debug the currently open LeetCode Python solution.
- Open or create a same-name `.txt` case file next to the solution.
- Read inputs from the case file and print PASS or FAIL results in the terminal.
- Stop cases that appear stuck in an infinite loop and report them in the terminal.
- Support common LeetCode helper types and judge wrappers such as `ListNode`, `TreeNode`, `Node`, `NestedInteger`, `Employee`, `Interval`, `Point`, `ArrayReader`, `BinaryMatrix`, and `MountainArray`.
- Infer common LeetCode helper inputs even when pasted code is missing some type annotations such as `TreeNode` or `ListNode`.
- Run multiple test cases from one file by separating cases with `---`.

## Requirements

- Visual Studio Code
- Python 3.9 or newer
- The VS Code `Python` and `Python Debugger` extensions

## Python Version

The extension runs with the Python interpreter selected in VS Code for the debug session.

- Supported: Python 3.9+
- Verified in this repository: Python 3.9, 3.13, and 3.14
- If the selected interpreter is older than Python 3.9, the debug session exits with a version error before running your solution

## Quick Start

1. Open a Python solution file such as `add_two_numbers.py`.
2. Run `LeetCode: Open Case File` from the Command Palette, or click the editor title button.
3. Fill in the generated `add_two_numbers.txt` file.
4. Set breakpoints in your Python solution.
5. Run `LeetCode: Debug Current Solution`.
6. Step through the code in the debugger and check the integrated terminal output.

## Case File Format

The extension looks for a `.txt` file with the same base name as the active Python file.

Example:

`add_two_numbers.py`

```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next

            carry, digit = divmod(total, 10)
            current.next = ListNode(digit)
            current = current.next

        return dummy.next
```

`add_two_numbers.txt`

```text
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
```

## Multiple Test Cases

Separate test cases with `---`.

```text
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
---
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

## Output

If expected output is present, the extension prints validation results:

```text
Case 1: PASS
expected: [7,0,8]
actual:   [7,0,8]
```

If you omit `Output:`, the extension prints the actual result only.

If a case exceeds the default timeout, the runtime stops it and prints `Case N: INFINITE LOOP`.
The default limit is 5 seconds of CPU time per case. You can override it with the `LEETCODE_DEBUG_TIMEOUT_SECONDS` environment variable, or disable it by setting that variable to `0`.

## Supported LeetCode Types

The runtime currently injects and converts these common LeetCode-only types for you:

- `ListNode`
- `TreeNode`
- `Node`
- `NestedInteger`
- `Employee`
- `Interval`
- `Point`
- `ImmutableListNode`
- `ArrayReader`
- `BinaryMatrix`
- `MountainArray`
- `HtmlParser`
- `Robot`
- `GridMaster`
- `Master`
- `CustomFunction`
- `Sea`

For `Node`, the runtime auto-detects the common LeetCode encodings:

- Binary tree node: `[1,2,3,null,4]`
- N-ary tree node: `[1,null,3,2,4,null,5,6]`
- Graph node: `[[2,4],[1,3],[2,4],[1,3]]`
- Random-pointer list node: `[[7,null],[13,0],[11,4],[10,2],[1,0]]`

Some judge interface types accept compact case-file values too:

- `BinaryMatrix`: `[[0,1],[1,1]]`
- `MountainArray`: `[1,5,2]`
- `ArrayReader`: `[1,1,1,0]`
- `Point`: `[x,y]`
- `Sea`: `[[x1,y1],[x2,y2]]`
- `CustomFunction`: `{"kind": "sum"}` or `{"kind": "product"}`

## Notes

- Your solution does not need `import leetcode` or a custom `run()` wrapper.
- LeetCode helper inputs are converted automatically from compact case-file literals.
- The extension looks for a `Solution` class and auto-detects the LeetCode entry method.
- Helper methods inside `Solution` are supported, and named `Input:` blocks can still run even if you renamed your method parameters.
- Common pasted solutions can still work even if `TreeNode` or `ListNode` type annotations were removed.
- Hidden global APIs such as `isBadVersion`, `knows`, or `read4` are not auto-mocked yet.

## Development

If you want to run this repository locally in VS Code's Extension Development Host:

1. Open this repo in VS Code.
2. Press `F5`.
3. A new Extension Development Host window will open with the extension loaded temporarily.

This is only for local development. Marketplace users can install the extension normally and use the quick-start flow above.
