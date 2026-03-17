#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import inspect
import json
import re
import sys
from collections import Counter, defaultdict, deque
from functools import cache, lru_cache
from pathlib import Path
from types import ModuleType, UnionType
from typing import Any, DefaultDict, Deque, Dict, List, Optional, Set, Tuple, Union, get_args, get_origin, get_type_hints


class ListNode:
    # @DontTrace
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next

    # @DontTrace
    def __repr__(self) -> str:
        next_value = None if self.next is None else self.next.val
        return f"ListNode(val={self.val}, next={next_value})"

    __str__ = __repr__


class TreeNode:
    # @DontTrace
    def __init__(
        self,
        val: int = 0,
        left: "TreeNode | None" = None,
        right: "TreeNode | None" = None,
    ):
        self.val = val
        self.left = left
        self.right = right

    # @DontTrace
    def __repr__(self) -> str:
        left_value = None if self.left is None else self.left.val
        right_value = None if self.right is None else self.right.val
        return f"TreeNode(val={self.val}, left={left_value}, right={right_value})"

    __str__ = __repr__


class Node:
    # @DontTrace
    def __init__(
        self,
        val: int = 0,
        left: "Node | None" = None,
        right: "Node | None" = None,
        next: "Node | None" = None,
        random: "Node | None" = None,
        children: list["Node"] | None = None,
        neighbors: list["Node"] | None = None,
        parent: "Node | None" = None,
        prev: "Node | None" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
        self.random = random
        self.children = list(children or [])
        self.neighbors = list(neighbors or [])
        self.parent = parent
        self.prev = prev

    # @DontTrace
    def __repr__(self) -> str:
        return f"Node(val={self.val})"

    __str__ = __repr__


class NestedInteger:
    # @DontTrace
    def __init__(self, value: Any = None):
        if isinstance(value, NestedInteger):
            value = value.to_python()

        if isinstance(value, int):
            self._integer = value
            self._list: list["NestedInteger"] | None = None
            return

        self._integer: int | None = None
        self._list: list["NestedInteger"] | None = []
        if value is None:
            return

        if not isinstance(value, list):
            raise TypeError("NestedInteger expects an int, list, or None.")

        for item in value:
            self.add(item if isinstance(item, NestedInteger) else NestedInteger(item))

    # @DontTrace
    def isInteger(self) -> bool:
        return self._integer is not None

    # @DontTrace
    def add(self, elem: "NestedInteger") -> None:
        if self._list is None:
            previous = self._integer
            self._integer = None
            self._list = []
            if previous is not None:
                self._list.append(NestedInteger(previous))

        self._list.append(elem if isinstance(elem, NestedInteger) else NestedInteger(elem))

    # @DontTrace
    def setInteger(self, value: int) -> None:
        self._integer = value
        self._list = None

    # @DontTrace
    def getInteger(self) -> int | None:
        return self._integer

    # @DontTrace
    def getList(self) -> list["NestedInteger"] | None:
        return self._list

    # @DontTrace
    def to_python(self) -> Any:
        if self.isInteger():
            return self._integer
        return [item.to_python() for item in self._list or []]

    # @DontTrace
    def __repr__(self) -> str:
        return f"NestedInteger({self.to_python()!r})"

    __str__ = __repr__


class Employee:
    # @DontTrace
    def __init__(self, id: int = 0, importance: int = 0, subordinates: list[int] | None = None):
        self.id = id
        self.importance = importance
        self.subordinates = list(subordinates or [])

    # @DontTrace
    def __repr__(self) -> str:
        return f"Employee(id={self.id}, importance={self.importance}, subordinates={self.subordinates})"

    __str__ = __repr__


class Interval:
    # @DontTrace
    def __init__(self, start: int = 0, end: int = 0):
        self.start = start
        self.end = end

    # @DontTrace
    def __repr__(self) -> str:
        return f"Interval(start={self.start}, end={self.end})"

    __str__ = __repr__


class Point:
    # @DontTrace
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    # @DontTrace
    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    __str__ = __repr__


class ImmutableListNode:
    # @DontTrace
    def __init__(self, val: int = 0, next: "ImmutableListNode | None" = None):
        self._val = val
        self._next = next

    # @DontTrace
    def printValue(self) -> None:
        print(self._val, end=" ")

    # @DontTrace
    def getNext(self) -> "ImmutableListNode | None":
        return self._next

    # @DontTrace
    def __repr__(self) -> str:
        next_value = None if self._next is None else self._next._val
        return f"ImmutableListNode(val={self._val}, next={next_value})"

    __str__ = __repr__


class BinaryMatrix:
    # @DontTrace
    def __init__(self, grid: list[list[int]]):
        self._grid = [list(row) for row in grid]

    # @DontTrace
    def get(self, row: int, col: int) -> int:
        return self._grid[row][col]

    # @DontTrace
    def dimensions(self) -> list[int]:
        return [len(self._grid), len(self._grid[0]) if self._grid else 0]

    # @DontTrace
    def to_python(self) -> list[list[int]]:
        return [list(row) for row in self._grid]


class MountainArray:
    # @DontTrace
    def __init__(self, values: list[int]):
        self._values = list(values)

    # @DontTrace
    def get(self, index: int) -> int:
        return self._values[index]

    # @DontTrace
    def length(self) -> int:
        return len(self._values)

    # @DontTrace
    def to_python(self) -> list[int]:
        return list(self._values)


class ArrayReader:
    # @DontTrace
    def __init__(self, values: list[int]):
        self._values = list(values)

    # @DontTrace
    def get(self, index: int) -> int:
        if index < 0 or index >= len(self._values):
            return 2147483647
        return self._values[index]

    # @DontTrace
    def compareSub(self, l: int, r: int, x: int, y: int) -> int:
        left_sum = sum(self._values[l : r + 1])
        right_sum = sum(self._values[x : y + 1])
        if left_sum == right_sum:
            return 0
        return 1 if left_sum > right_sum else -1

    # @DontTrace
    def query(self, a: int, b: int, c: int, d: int) -> int:
        counts = Counter(self._values[index] for index in (a, b, c, d))
        largest_group = max(counts.values()) if counts else 0
        if largest_group == 4:
            return 4
        if largest_group == 3:
            return 2
        return 0

    # @DontTrace
    def length(self) -> int:
        return len(self._values)

    # @DontTrace
    def to_python(self) -> list[int]:
        return list(self._values)


class HtmlParser:
    # @DontTrace
    def __init__(self, graph: dict[str, list[str]]):
        self._graph = {str(url): list(urls) for url, urls in graph.items()}

    # @DontTrace
    def getUrls(self, url: str) -> list[str]:
        return list(self._graph.get(url, []))

    # @DontTrace
    def to_python(self) -> dict[str, list[str]]:
        return {url: list(urls) for url, urls in self._graph.items()}


class Robot:
    # @DontTrace
    def __init__(self, room: list[list[Any]], row: int = 0, col: int = 0, direction: int = 0):
        self._room = [list(line) for line in room]
        self._row = row
        self._col = col
        self._direction = direction % 4
        self._cleaned: set[tuple[int, int]] = set()

    # @DontTrace
    def move(self) -> bool:
        delta_row, delta_col = [(-1, 0), (0, 1), (1, 0), (0, -1)][self._direction]
        next_row = self._row + delta_row
        next_col = self._col + delta_col
        if not self._is_open(next_row, next_col):
            return False
        self._row = next_row
        self._col = next_col
        return True

    # @DontTrace
    def turnLeft(self) -> None:
        self._direction = (self._direction - 1) % 4

    # @DontTrace
    def turnRight(self) -> None:
        self._direction = (self._direction + 1) % 4

    # @DontTrace
    def clean(self) -> None:
        self._cleaned.add((self._row, self._col))

    # @DontTrace
    def cleanedCells(self) -> list[list[int]]:
        return [[row, col] for row, col in sorted(self._cleaned)]

    # @DontTrace
    def to_python(self) -> dict[str, Any]:
        return {
            "room": [list(line) for line in self._room],
            "row": self._row,
            "col": self._col,
            "direction": self._direction,
            "cleaned": self.cleanedCells(),
        }

    # @DontTrace
    def _is_open(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row >= len(self._room) or col >= len(self._room[row]):
            return False
        cell = self._room[row][col]
        return cell not in (0, "#", "X", -1)


class GridMaster:
    # @DontTrace
    def __init__(
        self,
        grid: list[list[Any]],
        row: int = 0,
        col: int = 0,
        target: tuple[int, int] | None = None,
    ):
        self._grid = [list(line) for line in grid]
        self._row = row
        self._col = col
        self._target = target if target is not None else self._find_target()

    # @DontTrace
    def canMove(self, direction: str) -> bool:
        next_row, next_col = self._next_position(direction)
        return self._is_open(next_row, next_col)

    # @DontTrace
    def move(self, direction: str) -> int:
        if not self.canMove(direction):
            return -1
        self._row, self._col = self._next_position(direction)
        cell = self._grid[self._row][self._col]
        if isinstance(cell, (int, float)) and cell > 0:
            return int(cell)
        return 1

    # @DontTrace
    def isTarget(self) -> bool:
        return self._target == (self._row, self._col)

    # @DontTrace
    def to_python(self) -> dict[str, Any]:
        return {
            "grid": [list(line) for line in self._grid],
            "row": self._row,
            "col": self._col,
            "target": None if self._target is None else list(self._target),
        }

    # @DontTrace
    def _next_position(self, direction: str) -> tuple[int, int]:
        deltas = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
        delta_row, delta_col = deltas[direction]
        return self._row + delta_row, self._col + delta_col

    # @DontTrace
    def _is_open(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row >= len(self._grid) or col >= len(self._grid[row]):
            return False
        cell = self._grid[row][col]
        return cell not in (0, "#", "X", -1)

    # @DontTrace
    def _find_target(self) -> tuple[int, int] | None:
        for row_index, row in enumerate(self._grid):
            for col_index, cell in enumerate(row):
                if cell in ("T", 2):
                    return (row_index, col_index)
        return None


class Master:
    # @DontTrace
    def __init__(self, secret: str):
        self._secret = secret

    # @DontTrace
    def guess(self, word: str) -> int:
        if len(word) != len(self._secret):
            return -1
        return sum(left == right for left, right in zip(word, self._secret))


class CustomFunction:
    # @DontTrace
    def __init__(self, kind: str = "sum"):
        self._kind = kind

    # @DontTrace
    def f(self, x: int, y: int) -> int:
        if self._kind == "sum":
            return x + y
        if self._kind == "product":
            return x * y
        if self._kind == "max":
            return max(x, y)
        if self._kind == "min":
            return min(x, y)
        if self._kind == "pow":
            return x**y
        if self._kind == "xor":
            return x ^ y
        raise ValueError(f"Unsupported CustomFunction kind: {self._kind}")


class Sea:
    # @DontTrace
    def __init__(self, ships: list[list[int]]):
        self._ships = {tuple(point) for point in ships}

    # @DontTrace
    def hasShips(self, topRight: Point, bottomLeft: Point) -> bool:
        for ship_x, ship_y in self._ships:
            if bottomLeft.x <= ship_x <= topRight.x and bottomLeft.y <= ship_y <= topRight.y:
                return True
        return False

    # @DontTrace
    def to_python(self) -> list[list[int]]:
        return [list(point) for point in sorted(self._ships)]


LEETCODE_GLOBALS = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "Node": Node,
    "NestedInteger": NestedInteger,
    "Employee": Employee,
    "Interval": Interval,
    "Point": Point,
    "ImmutableListNode": ImmutableListNode,
    "BinaryMatrix": BinaryMatrix,
    "MountainArray": MountainArray,
    "ArrayReader": ArrayReader,
    "HtmlParser": HtmlParser,
    "Robot": Robot,
    "GridMaster": GridMaster,
    "Master": Master,
    "CustomFunction": CustomFunction,
    "Sea": Sea,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "Set": Set,
    "Tuple": Tuple,
    "Deque": Deque,
    "DefaultDict": DefaultDict,
    "deque": deque,
    "defaultdict": defaultdict,
    "Counter": Counter,
    "cache": cache,
    "lru_cache": lru_cache,
}


# @DontTrace
def create_compat_leetcode_module() -> ModuleType:
    module = ModuleType("leetcode")
    for name, value in LEETCODE_GLOBALS.items():
        setattr(module, name, value)
    module.run = lambda *args, **kwargs: 0
    return module


# @DontTrace
def enable_pydevd_trace_filters() -> None:
    try:
        from _pydevd_bundle import pydevd_dont_trace
    except Exception:
        return

    pydevd_dont_trace.trace_filter(True)


# @DontTrace
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Debug the active LeetCode solution against a case file."
    )
    parser.add_argument("--solution", required=True, help="Path to the Python solution file.")
    parser.add_argument("--case-file", required=True, help="Path to the same-name .txt case file.")
    parser.add_argument("--method", help="Optional Solution method name.")
    return parser.parse_args()


# @DontTrace
def split_cases(raw_text: str) -> list[str]:
    normalized = raw_text.replace("\r\n", "\n")
    parts = [part.strip() for part in re.split(r"(?m)^\s*---\s*$", normalized)]
    return [part for part in parts if part]


# @DontTrace
def split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    quote = ""
    escaped = False
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())

    for char in text:
        if quote:
            current.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
            continue

        if char in ("'", '"'):
            quote = char
            current.append(char)
            continue

        if char in openers:
            depth += 1
            current.append(char)
            continue

        if char in pairs:
            depth = max(0, depth - 1)
            current.append(char)
            continue

        if char == "," and depth == 0:
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
            continue

        current.append(char)

    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


# @DontTrace
def split_named_assignment(text: str) -> tuple[str, str] | None:
    depth = 0
    quote = ""
    escaped = False
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())

    for index, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
            continue

        if char in ("'", '"'):
            quote = char
            continue

        if char in openers:
            depth += 1
            continue

        if char in pairs:
            depth = max(0, depth - 1)
            continue

        if char == "=" and depth == 0:
            name = text[:index].strip()
            value = text[index + 1 :].strip()
            if name.isidentifier() and value:
                return name, value
            return None

    return None


# @DontTrace
def extract_case_sections(case_text: str) -> tuple[str, str | None]:
    lines = [line.strip() for line in case_text.splitlines() if line.strip()]
    if not lines:
        return "", None

    input_prefixes = ("input:", "your input:")
    output_prefixes = ("output:", "expected:", "expected output:")
    stop_prefixes = ("explanation:",)
    input_lines: list[str] = []
    output_lines: list[str] = []
    mode = ""

    for line in lines:
        lowered = line.lower()

        if lowered.startswith(input_prefixes):
            mode = "input"
            payload = line.split(":", 1)[1].strip()
            if payload:
                input_lines.append(payload)
            continue

        if lowered.startswith(output_prefixes):
            mode = "output"
            payload = line.split(":", 1)[1].strip()
            if payload:
                output_lines.append(payload)
            continue

        if lowered.startswith(stop_prefixes):
            if mode == "output":
                break
            mode = ""
            continue

        if mode == "input":
            input_lines.append(line)
            continue

        if mode == "output":
            output_lines.append(line)

    if input_lines:
        input_text = "\n".join(input_lines).strip()
    else:
        fallback_lines: list[str] = []
        for line in lines:
            lowered = line.lower()
            if lowered.startswith(output_prefixes + stop_prefixes):
                break
            fallback_lines.append(line)
        input_text = "\n".join(fallback_lines).strip()

    expected_text = "\n".join(output_lines).strip() or None
    return input_text, expected_text


# @DontTrace
def parse_literal(text: str) -> Any:
    stripped = text.strip()
    if not stripped:
        raise ValueError("Empty input")

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    try:
        return ast.literal_eval(stripped)
    except (SyntaxError, ValueError):
        normalized = re.sub(r"\bnull\b", "None", stripped)
        normalized = re.sub(r"\btrue\b", "True", normalized)
        normalized = re.sub(r"\bfalse\b", "False", normalized)
        return ast.literal_eval(normalized)


# @DontTrace
def parse_case_block(case_text: str, param_names: list[str]) -> tuple[list[Any], dict[str, Any]]:
    input_text, _ = extract_case_sections(case_text)
    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Empty test case")

    if len(lines) == 1:
        assignment_parts = split_top_level_commas(lines[0])
        assignments = [split_named_assignment(part) for part in assignment_parts]
        if assignment_parts and all(item is not None for item in assignments):
            kwargs = {
                name: parse_literal(raw_value)
                for name, raw_value in assignments
                if name is not None
            }
            return [], kwargs

        try:
            value = parse_literal(lines[0])
        except (SyntaxError, ValueError):
            if len(param_names) > 1 and len(assignment_parts) > 1:
                return [parse_literal(part) for part in assignment_parts], {}
            raise

        if isinstance(value, dict):
            if len(param_names) == 1 and set(value.keys()) != {param_names[0]}:
                return [value], {}
            if set(value.keys()).issubset(set(param_names)):
                return [], value
            return [value], {}

        if len(param_names) == 1:
            return [value], {}

        if isinstance(value, (list, tuple)) and len(value) == len(param_names):
            return list(value), {}

        return [value], {}

    if all("=" in line and line.split("=", 1)[0].strip().isidentifier() for line in lines):
        kwargs: dict[str, Any] = {}
        for line in lines:
            name, raw_value = line.split("=", 1)
            kwargs[name.strip()] = parse_literal(raw_value)
        return [], kwargs

    return [parse_literal(line) for line in lines], {}


# @DontTrace
def is_optional(annotation: Any) -> bool:
    origin = get_origin(annotation)
    return origin in (Union, UnionType) and type(None) in get_args(annotation)


# @DontTrace
def unwrap_optional(annotation: Any) -> Any:
    if is_optional(annotation):
        return next(arg for arg in get_args(annotation) if arg is not type(None))
    return annotation


# @DontTrace
def get_type_name(value_or_type: Any) -> str | None:
    if inspect.isclass(value_or_type):
        return getattr(value_or_type, "__name__", None)
    return value_or_type.__class__.__name__


# @DontTrace
def is_named_type(annotation: Any, type_name: str) -> bool:
    return get_type_name(annotation) == type_name


# @DontTrace
def is_named_instance(value: Any, type_name: str) -> bool:
    return get_type_name(value) == type_name


# @DontTrace
def build_linked_list(values: Any) -> ListNode | None:
    if values is None:
        return None
    if not isinstance(values, list):
        raise ValueError("Linked list input must be a list like [1,2,3].")

    dummy = ListNode()
    current = dummy
    for value in values:
        current.next = ListNode(value)
        current = current.next
    return dummy.next


# @DontTrace
def linked_list_to_list(node: Any) -> list[Any]:
    result = []
    current = node
    while current is not None:
        result.append(current.val)
        current = current.next
    return result


# @DontTrace
def build_tree(values: Any) -> TreeNode | None:
    if values is None:
        return None
    if not isinstance(values, list):
        raise ValueError("Tree input must be a list like [1,2,3,null,4].")
    if not values:
        return None

    iter_values = iter(values)
    root_value = next(iter_values)
    if root_value is None:
        return None

    root = TreeNode(root_value)
    queue = [root]
    for left_value, right_value in zip(iter_values, iter_values):
        node = queue.pop(0)
        if left_value is not None:
            node.left = TreeNode(left_value)
            queue.append(node.left)
        if right_value is not None:
            node.right = TreeNode(right_value)
            queue.append(node.right)

    if len(values) % 2 == 0:
        last_value = values[-1]
        if queue and last_value is not None:
            queue.pop(0).left = TreeNode(last_value)
    return root


# @DontTrace
def tree_to_list(root: Any) -> list[Any]:
    if root is None:
        return []

    result: list[Any] = []
    queue: list[Any | None] = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            result.append(None)
            continue
        result.append(node.val)
        queue.append(getattr(node, "left", None))
        queue.append(getattr(node, "right", None))

    while result and result[-1] is None:
        result.pop()
    return result


# @DontTrace
def build_binary_node_tree(values: Any) -> Node | None:
    if values is None:
        return None
    if not isinstance(values, list):
        raise ValueError("Binary Node tree input must be a list like [1,2,3,null,4].")
    if not values:
        return None

    iter_values = iter(values)
    root_value = next(iter_values)
    if root_value is None:
        return None

    root = Node(root_value)
    queue = [root]
    for left_value, right_value in zip(iter_values, iter_values):
        node = queue.pop(0)
        if left_value is not None:
            node.left = Node(left_value)
            queue.append(node.left)
        if right_value is not None:
            node.right = Node(right_value)
            queue.append(node.right)

    if len(values) % 2 == 0:
        last_value = values[-1]
        if queue and last_value is not None:
            queue.pop(0).left = Node(last_value)
    return root


# @DontTrace
def build_nary_tree(values: Any) -> Node | None:
    if values is None:
        return None
    if not isinstance(values, list):
        raise ValueError("N-ary Node input must be a list like [1,null,3,2,4,null,5,6].")
    if not values:
        return None

    root_value = values[0]
    if root_value is None:
        return None

    root = Node(root_value, children=[])
    if len(values) == 1:
        return root

    index = 2 if len(values) > 1 and values[1] is None else 1
    queue = deque([root])

    while queue and index <= len(values):
        parent = queue.popleft()
        children: list[Node] = []
        while index < len(values) and values[index] is not None:
            child = Node(values[index], children=[])
            children.append(child)
            queue.append(child)
            index += 1
        parent.children = children
        index += 1

    return root


# @DontTrace
def serialize_nary_tree(root: Any) -> list[Any]:
    if root is None:
        return []

    values: list[Any] = [root.val]
    queue = deque([root])
    while queue:
        parent = queue.popleft()
        values.append(None)
        for child in getattr(parent, "children", []) or []:
            values.append(child.val)
            queue.append(child)

    while values and values[-1] is None:
        values.pop()
    return values


# @DontTrace
def build_graph_node(adjacency: Any) -> Node | None:
    if adjacency is None:
        return None
    if not isinstance(adjacency, list):
        raise ValueError("Graph Node input must be an adjacency list like [[2,4],[1,3],[2,4],[1,3]].")
    if not adjacency:
        return None

    nodes = {index: Node(index, neighbors=[]) for index in range(1, len(adjacency) + 1)}
    for index, neighbor_values in enumerate(adjacency, start=1):
        if not isinstance(neighbor_values, list):
            raise ValueError("Each graph node must list its neighbor values.")
        nodes[index].neighbors = [nodes[neighbor] for neighbor in neighbor_values]
    return nodes[1]


# @DontTrace
def serialize_graph_node(node: Any) -> list[list[int]]:
    if node is None:
        return []

    discovered: dict[int, Any] = {}
    queue = deque([node])
    while queue:
        current = queue.popleft()
        if current is None or id(current) in discovered:
            continue
        discovered[id(current)] = current
        for neighbor in getattr(current, "neighbors", []) or []:
            queue.append(neighbor)

    ordered_nodes = sorted(discovered.values(), key=lambda item: item.val)
    return [
        [neighbor.val for neighbor in getattr(current, "neighbors", []) or []]
        for current in ordered_nodes
    ]


# @DontTrace
def build_random_list_node(pairs: Any) -> Node | None:
    if pairs is None:
        return None
    if not isinstance(pairs, list):
        raise ValueError("Random list input must be a list like [[7,null],[13,0],[11,4]].")
    if not pairs:
        return None

    nodes = [Node(item[0]) for item in pairs]
    for index, node in enumerate(nodes[:-1]):
        node.next = nodes[index + 1]

    for node, item in zip(nodes, pairs):
        random_index = item[1] if len(item) > 1 else None
        node.random = None if random_index is None else nodes[random_index]

    return nodes[0]


# @DontTrace
def serialize_random_list_node(head: Any) -> list[list[Any]]:
    nodes = []
    current = head
    while current is not None:
        nodes.append(current)
        current = current.next

    index_by_id = {id(node): index for index, node in enumerate(nodes)}
    return [
        [node.val, None if node.random is None else index_by_id[id(node.random)]]
        for node in nodes
    ]


# @DontTrace
def collect_node_features(root: Any) -> dict[str, bool]:
    queue = deque([root])
    seen: set[int] = set()
    features = {
        "has_left_right": False,
        "has_children": False,
        "has_neighbors": False,
        "has_random": False,
        "has_next": False,
    }

    while queue:
        node = queue.popleft()
        if node is None or id(node) in seen:
            continue
        seen.add(id(node))

        left = getattr(node, "left", None)
        right = getattr(node, "right", None)
        next_node = getattr(node, "next", None)
        random = getattr(node, "random", None)
        children = list(getattr(node, "children", []) or [])
        neighbors = list(getattr(node, "neighbors", []) or [])

        if left is not None or right is not None:
            features["has_left_right"] = True
        if children:
            features["has_children"] = True
        if neighbors:
            features["has_neighbors"] = True
        if random is not None:
            features["has_random"] = True
        if next_node is not None:
            features["has_next"] = True

        queue.extend([left, right, next_node, random])
        queue.extend(children)
        queue.extend(neighbors)

    return features


# @DontTrace
def detect_node_structure(node: Any) -> str:
    features = collect_node_features(node)
    if features["has_neighbors"]:
        return "graph"
    if features["has_children"] and not features["has_left_right"]:
        return "nary"
    if features["has_random"] and not features["has_left_right"] and not features["has_children"]:
        return "random_list"
    return "binary"


# @DontTrace
def build_nested_integer(value: Any) -> NestedInteger:
    return value if isinstance(value, NestedInteger) else NestedInteger(value)


# @DontTrace
def build_employee(value: Any) -> Employee:
    if isinstance(value, Employee):
        return value
    if isinstance(value, dict):
        return Employee(
            id=value.get("id", 0),
            importance=value.get("importance", 0),
            subordinates=value.get("subordinates", []),
        )
    if isinstance(value, (list, tuple)) and len(value) >= 3:
        return Employee(value[0], value[1], value[2])
    raise ValueError("Employee input must be [id, importance, subordinates] or a dict.")


# @DontTrace
def build_interval(value: Any) -> Interval:
    if isinstance(value, Interval):
        return value
    if isinstance(value, dict):
        return Interval(value.get("start", 0), value.get("end", 0))
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return Interval(value[0], value[1])
    raise ValueError("Interval input must be [start, end] or a dict.")


# @DontTrace
def build_point(value: Any) -> Point:
    if isinstance(value, Point):
        return value
    if isinstance(value, dict):
        return Point(value.get("x", 0), value.get("y", 0))
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return Point(value[0], value[1])
    raise ValueError("Point input must be [x, y] or a dict.")


# @DontTrace
def build_immutable_list_node(values: Any) -> ImmutableListNode | None:
    if values is None:
        return None
    if not isinstance(values, list):
        raise ValueError("ImmutableListNode input must be a list like [1,2,3].")

    dummy = ImmutableListNode()
    current = dummy
    for value in values:
        current._next = ImmutableListNode(value)
        current = current._next
    return dummy.getNext()


# @DontTrace
def immutable_list_to_list(node: Any) -> list[Any]:
    values = []
    current = node
    while current is not None:
        values.append(getattr(current, "_val", None))
        current = current.getNext()
    return values


# @DontTrace
def build_binary_matrix(value: Any) -> BinaryMatrix:
    grid = value.get("grid", value.get("matrix", value.get("values"))) if isinstance(value, dict) else value
    if not isinstance(grid, list):
        raise ValueError("BinaryMatrix input must be a 2D list or dict with grid/matrix.")
    return BinaryMatrix(grid)


# @DontTrace
def build_mountain_array(value: Any) -> MountainArray:
    values = value.get("values", value.get("array", value.get("mountain"))) if isinstance(value, dict) else value
    if not isinstance(values, list):
        raise ValueError("MountainArray input must be a list or dict with values/array.")
    return MountainArray(values)


# @DontTrace
def build_array_reader(value: Any) -> ArrayReader:
    values = value.get("values", value.get("array", value.get("data"))) if isinstance(value, dict) else value
    if not isinstance(values, list):
        raise ValueError("ArrayReader input must be a list or dict with values/array.")
    return ArrayReader(values)


# @DontTrace
def build_html_parser(value: Any) -> HtmlParser:
    graph = value.get("graph", {}) if isinstance(value, dict) and "graph" in value else value
    if not isinstance(graph, dict):
        raise ValueError("HtmlParser input must be a dict mapping URLs to outgoing URLs.")
    return HtmlParser(graph)


# @DontTrace
def build_robot(value: Any) -> Robot:
    if isinstance(value, dict):
        room = value.get("room", value.get("grid"))
        row = value.get("row", value.get("startRow", 0))
        col = value.get("col", value.get("startCol", 0))
        direction = value.get("direction", 0)
    else:
        room = value
        row = 0
        col = 0
        direction = 0

    if not isinstance(room, list):
        raise ValueError("Robot input must be a room grid or dict with room/grid.")
    return Robot(room, row=row, col=col, direction=direction)


# @DontTrace
def build_grid_master(value: Any) -> GridMaster:
    if isinstance(value, dict):
        grid = value.get("grid")
        row = value.get("row", value.get("startRow", 0))
        col = value.get("col", value.get("startCol", 0))
        target_value = value.get("target")
        target = None if target_value is None else tuple(target_value)
    else:
        grid = value
        row = 0
        col = 0
        target = None

    if not isinstance(grid, list):
        raise ValueError("GridMaster input must be a grid or dict with grid.")
    return GridMaster(grid, row=row, col=col, target=target)


# @DontTrace
def build_master(value: Any) -> Master:
    secret = value.get("secret") if isinstance(value, dict) else value
    if not isinstance(secret, str):
        raise ValueError("Master input must be a secret string or dict with secret.")
    return Master(secret)


# @DontTrace
def build_custom_function(value: Any) -> CustomFunction:
    if isinstance(value, dict):
        kind = value.get("kind", "sum")
    elif isinstance(value, str):
        kind = value
    else:
        kind = "sum"
    return CustomFunction(kind)


# @DontTrace
def build_sea(value: Any) -> Sea:
    ships = value.get("ships") if isinstance(value, dict) else value
    if not isinstance(ships, list):
        raise ValueError("Sea input must be a list of ship coordinates or dict with ships.")
    return Sea(ships)


# @DontTrace
def looks_like_random_list_input(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(
            isinstance(item, (list, tuple))
            and len(item) == 2
            and not isinstance(item[0], (list, dict))
            and (item[1] is None or (isinstance(item[1], int) and 0 <= item[1] < len(value)))
            for item in value
        )
    )


# @DontTrace
def looks_like_graph_input(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(
            isinstance(item, list)
            and all(isinstance(neighbor, int) and 1 <= neighbor <= len(value) for neighbor in item)
            for item in value
        )
    )


# @DontTrace
def looks_like_nary_tree_input(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 1 and value[1] is None


# @DontTrace
def build_node(value: Any, param_name: str | None = None) -> Node | None:
    if value is None:
        return None
    if param_name in {"head", "list", "linkedlist"} and looks_like_random_list_input(value):
        return build_random_list_node(value)
    if param_name in {"node", "graph"} and looks_like_graph_input(value):
        return build_graph_node(value)
    if param_name in {"root", "tree"} and looks_like_nary_tree_input(value):
        return build_nary_tree(value)
    if looks_like_random_list_input(value):
        return build_random_list_node(value)
    if looks_like_graph_input(value):
        return build_graph_node(value)
    if looks_like_nary_tree_input(value):
        return build_nary_tree(value)
    return build_binary_node_tree(value)


# @DontTrace
def convert_value(value: Any, annotation: Any, param_name: str | None = None) -> Any:
    if annotation in (inspect.Signature.empty, Any):
        return value

    annotation = unwrap_optional(annotation)
    type_name = get_type_name(annotation)

    if type_name == "ListNode":
        return build_linked_list(value)
    if type_name == "TreeNode":
        return build_tree(value)
    if type_name == "Node":
        return build_node(value, param_name=param_name)
    if type_name == "NestedInteger":
        return build_nested_integer(value)
    if type_name == "Employee":
        return build_employee(value)
    if type_name == "Interval":
        return build_interval(value)
    if type_name == "Point":
        return build_point(value)
    if type_name == "ImmutableListNode":
        return build_immutable_list_node(value)
    if type_name == "BinaryMatrix":
        return build_binary_matrix(value)
    if type_name == "MountainArray":
        return build_mountain_array(value)
    if type_name == "ArrayReader":
        return build_array_reader(value)
    if type_name == "HtmlParser":
        return build_html_parser(value)
    if type_name == "Robot":
        return build_robot(value)
    if type_name == "GridMaster":
        return build_grid_master(value)
    if type_name == "Master":
        return build_master(value)
    if type_name == "CustomFunction":
        return build_custom_function(value)
    if type_name == "Sea":
        return build_sea(value)

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin in (list, List):
        inner = args[0] if args else Any
        if not isinstance(value, list):
            return value
        return [convert_value(item, inner) for item in value]

    if origin in (tuple, Tuple):
        if not isinstance(value, (list, tuple)):
            return value
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(convert_value(item, args[0]) for item in value)
        converted = []
        for index, item in enumerate(value):
            inner = args[index] if index < len(args) else Any
            converted.append(convert_value(item, inner))
        return tuple(converted)

    if origin in (dict, Dict):
        key_type = args[0] if len(args) > 0 else Any
        value_type = args[1] if len(args) > 1 else Any
        if not isinstance(value, dict):
            return value
        return {
            convert_value(key, key_type): convert_value(item, value_type)
            for key, item in value.items()
        }

    if origin in (set, Set):
        inner = args[0] if args else Any
        if not isinstance(value, (list, set, tuple)):
            return value
        return {convert_value(item, inner) for item in value}

    if origin in (deque, Deque):
        inner = args[0] if args else Any
        if not isinstance(value, (list, tuple, deque)):
            return value
        return deque(convert_value(item, inner) for item in value)

    if origin in (defaultdict, DefaultDict):
        key_type = args[0] if len(args) > 0 else Any
        value_type = args[1] if len(args) > 1 else Any
        if not isinstance(value, dict):
            return value
        converted = {
            convert_value(key, key_type): convert_value(item, value_type)
            for key, item in value.items()
        }
        return defaultdict(lambda: None, converted)

    return value


# @DontTrace
def serialize_output(value: Any) -> Any:
    if is_named_instance(value, "ListNode"):
        return linked_list_to_list(value)
    if is_named_instance(value, "TreeNode"):
        return tree_to_list(value)
    if is_named_instance(value, "Node"):
        structure = detect_node_structure(value)
        if structure == "graph":
            return serialize_graph_node(value)
        if structure == "nary":
            return serialize_nary_tree(value)
        if structure == "random_list":
            return serialize_random_list_node(value)
        return tree_to_list(value)
    if is_named_instance(value, "NestedInteger"):
        return value.to_python()
    if is_named_instance(value, "Employee"):
        return {
            "id": value.id,
            "importance": value.importance,
            "subordinates": list(value.subordinates),
        }
    if is_named_instance(value, "Interval"):
        return [value.start, value.end]
    if is_named_instance(value, "Point"):
        return [value.x, value.y]
    if is_named_instance(value, "ImmutableListNode"):
        return immutable_list_to_list(value)
    if isinstance(value, (BinaryMatrix, MountainArray, ArrayReader, HtmlParser, Robot, GridMaster, Sea)):
        return value.to_python()
    if isinstance(value, Master):
        return "<Master>"
    if isinstance(value, CustomFunction):
        return "<CustomFunction>"
    if isinstance(value, tuple):
        return [serialize_output(item) for item in value]
    if isinstance(value, list):
        return [serialize_output(item) for item in value]
    if isinstance(value, deque):
        return [serialize_output(item) for item in value]
    if isinstance(value, set):
        return [serialize_output(item) for item in sorted(value, key=repr)]
    if isinstance(value, dict):
        return {str(key): serialize_output(item) for key, item in value.items()}
    return value


# @DontTrace
def format_output_text(value: Any) -> str:
    return json.dumps(
        serialize_output(value),
        ensure_ascii=False,
        separators=(",", ":"),
    )


# @DontTrace
def normalize_expected_output_text(text: str) -> str:
    try:
        return format_output_text(parse_literal(text))
    except (SyntaxError, ValueError):
        return text.strip()


# @DontTrace
def load_solution_module(solution_path: Path) -> ModuleType:
    source_text = solution_path.read_text(encoding="utf-8")
    module = ModuleType("leetcode_solution")
    module.__file__ = str(solution_path)
    for name, value in LEETCODE_GLOBALS.items():
        setattr(module, name, value)
    sys.modules["leetcode"] = create_compat_leetcode_module()
    code = compile(source_text, str(solution_path), "exec")
    exec(code, module.__dict__)
    return module


# @DontTrace
def find_solution_method(module: ModuleType, method_name: str | None) -> tuple[type, str]:
    solution_cls = getattr(module, "Solution", None)
    if solution_cls is None or not inspect.isclass(solution_cls):
        raise RuntimeError("Solution class was not found.")

    if method_name:
        if not hasattr(solution_cls, method_name):
            raise RuntimeError(f"Solution.{method_name} was not found.")
        return solution_cls, method_name

    candidates = [
        name
        for name, value in solution_cls.__dict__.items()
        if callable(value) and not name.startswith("_")
    ]
    if not candidates:
        raise RuntimeError("No public method was found in Solution.")
    if len(candidates) > 1:
        joined = ", ".join(candidates)
        raise RuntimeError(f"Multiple public methods found ({joined}). Use --method.")
    return solution_cls, candidates[0]


# @DontTrace
def invoke_solution(
    module: ModuleType, solution_cls: type, method_name: str, case_text: str
) -> Any:
    solution = solution_cls()
    method = getattr(solution, method_name)
    signature = inspect.signature(method)
    params = list(signature.parameters.values())
    param_names = [param.name for param in params]
    raw_args, raw_kwargs = parse_case_block(case_text, param_names)
    type_hints = get_type_hints(method, globalns=module.__dict__, localns=module.__dict__)

    if raw_kwargs:
        converted_kwargs = {
            name: convert_value(
                value,
                type_hints.get(name, inspect.Signature.empty),
                param_name=name,
            )
            for name, value in raw_kwargs.items()
        }
        return method(**converted_kwargs)

    if len(raw_args) != len(params):
        expected = ", ".join(param_names)
        raise RuntimeError(
            f"Expected {len(params)} argument(s) ({expected}), got {len(raw_args)}."
        )

    converted_args = [
        convert_value(
            value,
            type_hints.get(param.name, inspect.Signature.empty),
            param_name=param.name,
        )
        for param, value in zip(params, raw_args)
    ]
    return method(*converted_args)


# @DontTrace
def evaluate_module_cases(
    module: ModuleType, method_name: str | None, raw_input: str
) -> tuple[int, str]:
    solution_cls, method_name = find_solution_method(module, method_name)
    outputs = []
    validations = []
    mismatch_found = False

    for index, case_text in enumerate(split_cases(raw_input), start=1):
        result = invoke_solution(module, solution_cls, method_name, case_text)
        actual_text = format_output_text(result)
        _, expected_text = extract_case_sections(case_text)

        if expected_text is None:
            outputs.append(actual_text)
            continue

        normalized_expected = normalize_expected_output_text(expected_text)
        is_match = actual_text == normalized_expected
        if not is_match:
            mismatch_found = True

        validations.append(
            "\n".join(
                [
                    f"Case {index}: {'PASS' if is_match else 'FAIL'}",
                    f"expected: {normalized_expected}",
                    f"actual:   {actual_text}",
                ]
            )
        )

    if validations:
        return (1 if mismatch_found else 0), "\n\n".join(validations)

    return 0, "\n".join(outputs)


# @DontTrace
def main() -> int:
    enable_pydevd_trace_filters()
    args = parse_args()
    solution_path = Path(args.solution).expanduser().resolve()
    case_file_path = Path(args.case_file).expanduser().resolve()

    if not solution_path.exists():
        raise RuntimeError(f"Solution file not found: {solution_path}")
    if not case_file_path.exists():
        raise RuntimeError(f"Case file not found: {case_file_path}")

    raw_input = case_file_path.read_text(encoding="utf-8").strip()
    if not raw_input:
        raise RuntimeError(f"Case file is empty: {case_file_path}")

    module = load_solution_module(solution_path)
    exit_code, output_text = evaluate_module_cases(module, args.method, raw_input)
    if output_text:
        print(output_text)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
