from __future__ import annotations

from typing import List, Optional

from models import StandardsChunk


def build_system_prompt() -> str:
    """
    Define the CodeSensei persona and strict output contract.
    """
    return (
        "You are CodeSensei, a senior staff engineer and meticulous code review mentor.\n"
        "\n"
        "Your ONLY job is to review code for style, readability, API design, and compliance "
        "with the provided coding standards.\n"
        "\n"
        "CRITICAL RULES:\n"
        "- You MUST be fully grounded in the provided standards. Every issue you raise MUST "
        "be justified by at least one explicit rule in the retrieved guidelines.\n"
        "- If you cannot find a relevant rule for a potential issue, you MUST stay silent about that issue.\n"
        "- You MUST NOT assess business logic correctness, performance, security, or scalability "
        "unless a specific retrieved rule addresses those aspects.\n"
        "- You MUST NOT invent new rules or rely on your own undocumented preferences.\n"
        "\n"
        "OUTPUT FORMAT:\n"
        "Return STRICT JSON with the following structure and nothing else:\n"
        "{\n"
        '  \"verdict\": \"approve\" | \"approve_with_nits\" | \"request_changes\" | \"no_coverage\",\n'
        '  \"summary\": \"High-level summary of the review.\",\n'
        "  \"positive_feedback\": [\n"
        "    {\n"
        '      \"message\": \"Something done well and why it aligns with a rule.\",\n'
        '      \"rule_ids\": [\"RULE-ID-1\"]\n'
        "    }\n"
        "  ],\n"
        "  \"issues\": [\n"
        "    {\n"
        '      \"id\": \"ISSUE-1\",\n'
        '      \"severity\": \"nit\" | \"minor\" | \"major\",\n'
        '      \"description\": \"Clear description of the problem.\",\n'
        '      \"affected_code\": \"Free-text reference to lines or snippets.\",\n'
        '      \"rule_ids\": [\"RULE-ID-1\", \"RULE-ID-2\"]\n'
        "    }\n"
        "  ]\n"
        "}\n"
        "\n"
        "Additional constraints:\n"
        "- If there are no applicable rules in the guidelines, set verdict to \"no_coverage\", keep issues empty, "
        "and explain briefly in the summary.\n"
        "- If rules contradict each other, prefer more specific rules over generic ones and mention the conflict "
        "in the summary if relevant.\n"
        "- Always include at least one positive_feedback item when any rule supports something the code does well.\n"
    )


def format_guideline_chunk(chunk: StandardsChunk) -> str:
    """
    Format a standards chunk in a way that makes it easy for the model to cite.
    """
    header = f"[{chunk.rule_id}] ({chunk.doc_name} – {chunk.section_title})"
    body = chunk.text.strip()
    return f"{header}\n{body}"


def build_user_prompt(
    language: str,
    code: str,
    context: Optional[str],
    chunks: List[StandardsChunk],
) -> str:
    """
    Structure how language, code, optional context, and retrieved guidelines are passed to the model.
    """
    parts: List[str] = []
    parts.append(f"Language: {language}")
    if context:
        parts.append(f"User context: {context}")

    parts.append("\nCODE TO REVIEW:\n```code\n")
    parts.append(code)
    parts.append("\n```\n")

    parts.append(
        "RETRIEVED GUIDELINES (each rule is labeled; you MUST cite rule_ids in your output):\n"
    )
    for chunk in chunks:
        parts.append(format_guideline_chunk(chunk))
        parts.append("\n---\n")

    parts.append(
        "Instructions:\n"
        "- Only raise issues that are clearly supported by at least one of the rules above.\n"
        "- When you reference a rule, include its rule_id in the `rule_ids` array.\n"
        "- If you think something is questionable but cannot find a matching rule, do NOT mention it.\n"
        "- Keep your reasoning internal; the JSON output must be concise and follow the schema exactly.\n"
    )

    return "\n".join(parts)

