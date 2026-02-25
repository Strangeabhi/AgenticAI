from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from models import StandardsChunk


def _parse_standards_file(path: Path) -> List[StandardsChunk]:
    """
    Very lightweight parser that treats each "Rule ID:" block in the markdown file
    as a single chunk. This keeps each rule self-contained and easy to cite.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    chunks: List[StandardsChunk] = []
    current_rule_id: str | None = None
    current_scope: str = "all-languages"
    current_body_lines: List[str] = []

    # Use the first markdown heading as a section title, if present.
    section_title = path.stem.replace("_", " ").title()
    for line in lines:
        if line.startswith("# "):
            section_title = line.lstrip("# ").strip()
            continue

        if line.strip().startswith("Rule ID:"):
            # Flush previous rule, if any.
            if current_rule_id and current_body_lines:
                chunks.append(
                    StandardsChunk(
                        rule_id=current_rule_id,
                        scope=current_scope,
                        doc_name=path.name,
                        section_title=section_title,
                        text="\n".join(current_body_lines).strip(),
                    )
                )
                current_body_lines = []

            # Start a new rule.
            current_rule_id = line.split("Rule ID:", 1)[1].strip()
            current_scope = "all-languages"
            continue

        if line.strip().startswith("Scope:"):
            current_scope = line.split("Scope:", 1)[1].strip()
            continue

        # Accumulate remaining content as body for the current rule.
        if current_rule_id:
            current_body_lines.append(line)

    # Flush last rule.
    if current_rule_id and current_body_lines:
        chunks.append(
            StandardsChunk(
                rule_id=current_rule_id,
                scope=current_scope,
                doc_name=path.name,
                section_title=section_title,
                text="\n".join(current_body_lines).strip(),
            )
        )

    return chunks


def load_standards_corpus(standards_dir: Path) -> List[StandardsChunk]:
    """
    Load all markdown documents from the standards directory and return a flat list of chunks.
    """
    if not standards_dir.exists():
        raise FileNotFoundError(f"Standards directory not found: {standards_dir}")

    chunks: List[StandardsChunk] = []
    for md_path in standards_dir.glob("*.md"):
        chunks.extend(_parse_standards_file(md_path))

    if not chunks:
        raise RuntimeError(f"No standards rules found in: {standards_dir}")

    return chunks


def filter_chunks_for_language(chunks: Iterable[StandardsChunk], language: str) -> List[StandardsChunk]:
    """
    Filter chunks by language based on their 'scope' field. Scopes can be:
    - 'all-languages'
    - specific language names ('python', 'javascript', 'typescript')
    - comma-separated lists like 'javascript,typescript'
    - domain scopes like 'http-apis'
    """
    language_norm = language.lower().strip()
    result: List[StandardsChunk] = []
    for chunk in chunks:
        scope = chunk.scope.lower()
        # Always include global rules.
        if "all-languages" in scope:
            result.append(chunk)
            continue

        # Direct language match or in a comma-delimited list.
        scopes = [s.strip() for s in scope.split(",")]
        if language_norm in scopes:
            result.append(chunk)

    return result

