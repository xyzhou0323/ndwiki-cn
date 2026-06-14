#!/usr/bin/env python3
"""Sync wiki/ (zh-hans) → wiki-zh-hant/ (zh-hant) via OpenCC.

Usage:
  python .llm-wiki/sync-zh-hant.py          # incremental: changed files only
  python .llm-wiki/sync-zh-hant.py --full   # convert all pages
  python .llm-wiki/sync-zh-hant.py --dry-run  # preview without writing
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import opencc

WIKI_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = WIKI_ROOT / "wiki"
DST_DIR = WIKI_ROOT / "wiki-zh-hant"
STATE_FILE = WIKI_ROOT / ".llm-wiki" / "zh-hant-state.json"

converter = opencc.OpenCC("s2t")  # Simplified → Traditional

# Files in wiki-zh-hant/ with hant-original content — never overwrite by auto-conversion.
# These exist in both repos but the hant version is manually authored, not s2t from zh-hans.
HANT_ORIGINAL = {
    "COLLABORATING.md",
    "README.md",
}


def to_hant(path: str) -> str:
    """Convert a relative path (from wiki/) to Traditional."""
    parts = Path(path).parts
    converted = [converter.convert(p) for p in parts]
    return str(Path(*converted))


def hant_filename(simplified_rel: str) -> str:
    """Full Traditional path under wiki-zh-hant/."""
    return str(DST_DIR / to_hant(simplified_rel))


def convert_content(text: str, simplified_rel: str) -> str:
    """Convert page content to Traditional, add zh-hans frontmatter link."""
    # Convert body
    text = converter.convert(text)

    # Add/update zh-hans in frontmatter
    rel_no_ext = str(Path(simplified_rel).with_suffix(""))
    zh_link = f"[[wiki/{rel_no_ext}]]"

    if "zh-hans:" in text:
        text = re.sub(r"zh-hans:.*", f"zh-hans: {zh_link}", text)
    else:
        # Insert after the first frontmatter field (after '---' line)
        fm_end = text.index("---", 4)  # second ---
        insertion = f"zh-hans: {zh_link}\n"
        text = text[:fm_end] + insertion + text[fm_end:]

    return text


def mark_needs_review(text: str) -> str:
    """Set needs-review: true in frontmatter."""
    if "needs-review:" in text:
        text = re.sub(r"needs-review:.*", "needs-review: true", text)
    else:
        fm_end = text.index("---", 4)
        text = text[:fm_end] + "needs-review: true\n" + text[fm_end:]
    return text


def clear_needs_review(text: str) -> str:
    """Remove needs-review from frontmatter."""
    return re.sub(r"needs-review: true\n", "", text)


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def get_all_pages() -> list[str]:
    """List all .md files under wiki/, relative paths."""
    pages = []
    for f in sorted(SRC_DIR.rglob("*.md")):
        rel = str(f.relative_to(SRC_DIR))
        pages.append(rel)
    return pages


def get_changed_pages() -> list[str]:
    """Get wiki/ .md files changed since last sync."""
    state = load_state()
    last_commit = state.get("last_commit", "")

    if not last_commit:
        return get_all_pages()

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{last_commit}..HEAD", "--", "wiki/"],
            capture_output=True, text=True, cwd=WIKI_ROOT,
        )
        files = [f for f in result.stdout.strip().split("\n") if f.endswith(".md")]
        # Convert to relative paths from wiki/
        return [f.replace("wiki/", "", 1) for f in files]
    except Exception:
        return get_all_pages()


def get_deleted_pages() -> list[str]:
    """Get wiki/ .md files deleted since last sync."""
    state = load_state()
    last_commit = state.get("last_commit", "")

    if not last_commit:
        return []

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=D",
             f"{last_commit}..HEAD", "--", "wiki/"],
            capture_output=True, text=True, cwd=WIKI_ROOT,
        )
        return [f for f in result.stdout.strip().split("\n") if f.endswith(".md")]
    except Exception:
        return []


def get_current_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=WIKI_ROOT,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def sync_file(simplified_rel: str, mark_review: bool = False, dry_run: bool = False):
    """Convert one page and write to zh-hant."""
    if simplified_rel in HANT_ORIGINAL:
        if not dry_run:
            print(f"  SKIP {simplified_rel} (hant-original, manually maintained)")
        return

    src_path = SRC_DIR / simplified_rel
    if not src_path.exists():
        return

    dst_path = Path(hant_filename(simplified_rel))

    if dry_run:
        print(f"  [dry-run] {simplified_rel} → {dst_path.relative_to(WIKI_ROOT)}")
        return

    text = src_path.read_text(encoding="utf-8")
    text = convert_content(text, simplified_rel)
    if mark_review:
        text = mark_needs_review(text)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(text, encoding="utf-8")


def remove_file(simplified_rel: str, dry_run: bool = False):
    """Remove the corresponding zh-hant page."""
    if simplified_rel in HANT_ORIGINAL:
        return  # never delete hant-original files

    dst_path = Path(hant_filename(simplified_rel))
    if dst_path.exists():
        if dry_run:
            print(f"  [dry-run] rm {dst_path.relative_to(WIKI_ROOT)}")
        else:
            dst_path.unlink()
            print(f"  RM {dst_path.relative_to(WIKI_ROOT)}")


def commit_sync(changed: list[str], deleted: list[str], dry_run: bool = False):
    """Commit and push changes in the zh-hant submodule."""
    if dry_run:
        print(f"\n  [dry-run] Would commit {len(changed)} changed + {len(deleted)} deleted in {DST_DIR}")
        return

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=DST_DIR,
        )
        if not result.stdout.strip():
            print("\n  No changes to commit in zh-hant submodule.")
            return

        subprocess.run(["git", "add", "-A"], cwd=DST_DIR, check=True)

        msg_lines = ["sync: zh-hans → zh-hant OpenCC conversion\n"]
        if changed:
            changed_preview = ", ".join(changed[:5])
            msg_lines.append(f"  {len(changed)} pages converted")
            if len(changed) > 5:
                msg_lines.append(f"  (incl. {changed_preview} ...)")
            else:
                msg_lines.append(f"  ({changed_preview})")
        if deleted:
            deleted_preview = ", ".join(deleted[:3])
            msg_lines.append(f"  {len(deleted)} pages removed ({deleted_preview})")

        subprocess.run(
            ["git", "commit", "-m", "\n".join(msg_lines)],
            cwd=DST_DIR, check=True,
        )

        subprocess.run(["git", "push"], cwd=DST_DIR, check=True)
        print(f"\n  Committed and pushed to ndwiki-hant.")
    except subprocess.CalledProcessError as e:
        print(f"\n  Warning: Failed to commit/push in submodule: {e}")


def main():
    dry_run = "--dry-run" in sys.argv
    full = "--full" in sys.argv
    do_push = "--push" in sys.argv

    action = "full" if full else "incremental"
    prefix = "[dry-run] " if dry_run else ""

    if full:
        pages = get_all_pages()
        print(f"{prefix}Full sync: {len(pages)} pages")
    else:
        changed = get_changed_pages()
        deleted_pages = get_deleted_pages()
        # Filter to just .md files relative to wiki/
        changed = [f for f in changed if not f.startswith("wiki/") or True]
        # Actually, git diff output is "wiki/01-基础/页.md" format
        # We already stripped "wiki/" prefix in get_changed_pages
        print(f"{prefix}Incremental sync: {len(changed)} changed, {len(deleted_pages)} deleted")

    pages = get_all_pages() if full else get_changed_pages()
    deleted = [] if full else get_deleted_pages()

    # Create destination root
    if not dry_run:
        DST_DIR.mkdir(parents=True, exist_ok=True)

    # Convert changed/new pages
    for rel in pages:
        sync_file(rel, mark_review=(not full), dry_run=dry_run)

    # Remove deleted pages
    for rel in deleted:
        remove_file(rel, dry_run=dry_run)

    # Commit and push to Traditional sub-repo (if --push)
    if do_push:
        commit_sync(pages, deleted, dry_run=dry_run)

    # Update state
    if not dry_run:
        state = load_state()
        state["last_commit"] = get_current_commit()
        state["last_sync"] = datetime.now().isoformat()
        state["page_count"] = len(pages) if full else state.get("page_count", 0)
        save_state(state)

    print(f"\n{prefix}Done. {len(pages)} converted, {len(deleted)} removed.")
    if not full and not dry_run:
        print("Pages with content changes marked `needs-review: true`.")
    if not do_push and not dry_run:
        print("Run with --push to commit and push changes to ndwiki-hant.")


if __name__ == "__main__":
    main()
