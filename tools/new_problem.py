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

        // System.out.println(answer);
    }}
}}
"""

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "problem"

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True

def md_link(text: str, url: str) -> str:
    if url.strip():
        return f"[{text}]({url})"
    return text

def update_between_markers(file_path: Path, start_marker: str, end_marker: str, new_block: str) -> None:
    if not file_path.exists():
        raise SystemExit(f"Missing file: {file_path}")

    content = file_path.read_text(encoding="utf-8")
    s = content.find(start_marker)
    e = content.find(end_marker)

    if s == -1 or e == -1 or e < s:
        raise SystemExit(
            f"Markers not found or invalid in {file_path.name}.\n"
            f"Add:\n{start_marker}\n...\n{end_marker}"
        )

    before = content[: s + len(start_marker)]
    middle = "\n" + new_block.rstrip() + "\n"
    after = content[e:]
    file_path.write_text(before + middle + after, encoding="utf-8")

def append_problem_row_to_readme(
    readme_path: Path,
    date: str,
    platform: str,
    problem_id: str,
    title: str,
    category: str,
    link: str,
    py_rel: str | None,
    java_rel: str | None,
) -> None:
    start = "<!-- AUTO:PROBLEMS:START -->"
    end = "<!-- AUTO:PROBLEMS:END -->"

    content = readme_path.read_text(encoding="utf-8")
    s = content.find(start)
    e = content.find(end)
    if s == -1 or e == -1 or e < s:
        raise SystemExit(
            f"Markers not found in README.md.\n"
            f"Add a problems section with:\n{start}\n...\n{end}"
        )

    block = content[s + len(start):e].strip("\n")

    # Ensure header exists
    if "| 날짜 |" not in block:
        # Create a fresh table header if missing
        table = [
            "| 날짜 | 플랫폼 | 문제 | 유형 | Python | Java |",
            "|---|---|---|---|---|---|",
        ]
        existing_rows = []
    else:
        lines = [ln for ln in block.splitlines() if ln.strip()]
        # Keep header (2 lines) + existing rows
        table = lines[:2]
        existing_rows = lines[2:]

    problem_cell = md_link(f"{problem_id} {title}", link) if link else f"{problem_id} {title}"
    py_cell = md_link("풀이", py_rel) if py_rel else "-"
    java_cell = md_link("풀이", java_rel) if java_rel else "-"

    new_row = f"| {date} | {platform} | {problem_cell} | {category} | {py_cell} | {java_cell} |"

    # Avoid duplicates (same platform+id)
    key = f"{platform} | {problem_id} "
    if any(key in r for r in existing_rows):
        return  # already recorded

    updated_rows = [new_row] + existing_rows  # newest first
    new_block = "\n".join(table + updated_rows)

    update_between_markers(readme_path, start, end, new_block)

def append_daily_log(
    weekly_path: Path,
    date: str,
    platform: str,
    problem_id: str,
    title: str,
    category: str,
    link: str,
    py_rel: str | None,
    java_rel: str | None,
) -> None:
    start = "<!-- AUTO:DAILY:START -->"
    end = "<!-- AUTO:DAILY:END -->"

    content = weekly_path.read_text(encoding="utf-8")
    s = content.find(start)
    e = content.find(end)
    if s == -1 or e == -1 or e < s:
        raise SystemExit(
            f"Markers not found in WEEKLY_LOG.md.\n"
            f"Add:\n{start}\n...\n{end}"
        )

    block = content[s + len(start):e].strip("\n")
    lines = [ln for ln in block.splitlines() if ln.strip()]

    # Find or create today's section
    date_header = f"### {date}"
    item = f"- [{platform}] {md_link(f'{problem_id} {title}', link)} · `{category}`" \
           f" · Python: {md_link('link', py_rel) if py_rel else '-'}" \
           f" · Java: {md_link('link', java_rel) if java_rel else '-'}"

    if date_header in lines:
        # Insert item right under today's header if not present
        idx = lines.index(date_header)
        # Scan until next header or end
        j = idx + 1
        while j < len(lines) and not lines[j].startswith("### "):
            if problem_id in lines[j] and platform in lines[j]:
                return  # already logged today
            j += 1
        lines.insert(idx + 1, item)
    else:
        # Prepend new date section at top
        new_section = [date_header, item, ""]
        lines = new_section + lines

    new_block = "\n".join(lines).rstrip()
    update_between_markers(weekly_path, start, end, new_block)

def main():
    ap = argparse.ArgumentParser(description="Create templates + auto-update README + WEEKLY_LOG.")
    ap.add_argument("--platform", default="BOJ", choices=["BOJ", "Programmers", "LeetCode"])
    ap.add_argument("--id", required=True, help="Problem ID (e.g., 1260 or P_42576)")
    ap.add_argument("--title", required=True, help="Problem title (Korean/English OK)")
    ap.add_argument("--category", required=True, help=f"One of: {', '.join(CATEGORIES.keys())}")
    ap.add_argument("--link", default="", help="Problem link")
    ap.add_argument("--lang", default="both", choices=["python", "java", "both"])
    ap.add_argument("--update-readme", action="store_true", help="Add a row to README.md table")
    ap.add_argument("--update-weekly", action="store_true", help="Add an item to WEEKLY_LOG.md for today")
    args = ap.parse_args()

    category_dir = CATEGORIES.get(args.category)
    if not category_dir:
        raise SystemExit(f"Unknown category: {args.category}\nUse one of: {', '.join(CATEGORIES.keys())}")

    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(args.title)

    root = Path(__file__).resolve().parents[1]  # repo root
    py_dir = root / "python" / category_dir
    java_dir = root / "java" / category_dir

    ensure_dir(py_dir)
    ensure_dir(java_dir)

    base = f"{args.platform}_{args.id}_{slug}"
    py_path = py_dir / f"{base}.py"
    java_path = java_dir / f"{base}.java"

    created = []
    py_rel = None
    java_rel = None

    if args.lang in ("python", "both"):
        content = PY_TEMPLATE.format(
            platform=args.platform,
            problem_id=args.id,
            title=args.title,
            link=args.link,
            category=args.category,
            date=date,
        )
        if write_if_missing(py_path, content):
            created.append(str(py_path.relative_to(root)))
        py_rel = str(py_path.relative_to(root))

    if args.lang in ("java", "both"):
        content = JAVA_TEMPLATE.format(
            platform=args.platform,
            problem_id=args.id,
            title=args.title,
            link=args.link,
            category=args.category,
            date=date,
        )
        if write_if_missing(java_path, content):
            created.append(str(java_path.relative_to(root)))
        java_rel = str(java_path.relative_to(root))

    # Auto-update README/WEEKLY_LOG if requested
    if args.update_readme:
        readme_path = root / "README.md"
        append_problem_row_to_readme(
            readme_path=readme_path,
            date=date,
            platform=args.platform,
            problem_id=args.id,
            title=args.title,
            category=args.category,
            link=args.link,
            py_rel=py_rel if args.lang in ("python", "both") else None,
            java_rel=java_rel if args.lang in ("java", "both") else None,
        )

    if args.update_weekly:
        weekly_path = root / "WEEKLY_LOG.md"
        append_daily_log(
            weekly_path=weekly_path,
            date=date,
            platform=args.platform,
            problem_id=args.id,
            title=args.title,
            category=args.category,
            link=args.link,
            py_rel=py_rel if args.lang in ("python", "both") else None,
            java_rel=java_rel if args.lang in ("java", "both") else None,
        )

    if created:
        print("✅ Created:")
        for c in created:
            print(" -", c)
    else:
        print("ℹ️ No new files (already exist).")

    if args.update_readme:
        print("✅ README.md updated.")
    if args.update_weekly:
        print("✅ WEEKLY_LOG.md updated.")

if __name__ == "__main__":
    main()
