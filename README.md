# LeetCode Debugger

Debug the active LeetCode Python solution in VS Code with a same-name `.txt` case file.

This repo is meant to be run in VS Code's Extension Development Host. You do not need to install or package anything. Open this repo in VS Code, press `F5`, and a new popup window will open with the extension loaded temporarily.

## Demo

- [YouTube demo video](https://youtu.be/1TlWg2j0BHs?si=dUUn1lnR8m786qIE)

## Features

- Debug the currently open LeetCode Python solution.
- Open or create a same-name `.txt` case file next to the solution.
- Read inputs from the case file and print PASS or FAIL results in the terminal.
- Support common LeetCode helper types and judge wrappers such as `ListNode`, `TreeNode`, `Node`, `NestedInteger`, `Employee`, `Interval`, `Point`, `ArrayReader`, `BinaryMatrix`, and `MountainArray`.
- Run multiple test cases from one file by separating cases with `---`.

## Requirements

- Visual Studio Code
- Python 3 available as `python3`
- The VS Code `Python` and `Python Debugger` extensions

The popup window will prompt for the Python extensions if they are missing.

## Quick Start on macOS

1. Open this repo in VS Code.
2. Press `F5`.
3. A new Extension Development Host window will open.
4. In that popup window, open the folder where your LeetCode Python files live.
5. Open a Python solution file such as `add_two_numbers.py`.
6. Run `LeetCode: Open Case File` from the Command Palette, or click the editor title button.
7. Fill in the generated `add_two_numbers.txt` file.
8. Set breakpoints in your Python solution.
9. Run `LeetCode: Debug Current Solution`.
10. Step through the code in the debugger and check the integrated terminal output.

You can close the popup whenever you're done. Nothing gets permanently installed into your main VS Code setup.

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
- The extension looks for a `Solution` class and runs its single public method.
- If your `Solution` class has multiple public methods, the runtime cannot pick one automatically.
- Hidden global APIs such as `isBadVersion`, `knows`, or `read4` are not auto-mocked yet.
