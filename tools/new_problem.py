# tools/new_problem.py
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


CATEGORIES = {
    "brute_force": "brute_force",
    "implementation": "implementation",
    "data_structure": "data_structure",
    "dfs_bfs": "dfs_bfs",
    "greedy": "greedy",
    "dp": "dynamic_programming",
    "graph": "graph",
    "binary_search": "binary_search",
}

PY_TEMPLATE = """\"\"\"{platform} {problem_id} - {title}
Link: {link}
Category: {category}
Date: {date}

Approach:
- 

Complexity:
- Time: 
- Space: 
\"\"\"

import sys

def input():
    return sys.stdin.readline().rstrip()

def main():
    # TODO: implement
    pass

if __name__ == "__main__":
    main()
"""

JAVA_TEMPLATE = """/*
{platform} {problem_id} - {title}
Link: {link}
Category: {category}
Date: {date}

Approach:
- 

Complexity:
- Time:
- Space:
*/

import java.io.*;
import java.util.*;

public class Main {{
    public static void main(String[] args) throws Exception {{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        // TODO: implement

        System.out.println();
    }}
}}
"""

NOTION_MD_TEMPLATE = """## 📍 문제 정보
- 문제명: {title}
- 출처: {platform}
- 링크: {link}
- 난이도: 
- 유형: {category}
- 날짜: {date}

---

## 🧩 문제 핵심
- 

---

## 🧠 접근 사고 과정
1. 
2. 
3. 

---

## ⏱️ 시간 / 공간 복잡도
- Time: 
- Space: 

---

## 🐍 Python 풀이
```python
# {py_path}
