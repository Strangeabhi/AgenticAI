def build_prompt(user_query: str) -> str:

    return f"""
You are a structured product query normalizer.

Return ONLY valid JSON.

STRICT RULES:
- No explanation
- No markdown
- Output must start with {{
- Output must end with }}
- Use null if unknown
- feature_preferences and missing_fields MUST be arrays

JSON Schema:
{{
  "product_type": string or null,
  "price_range": {{
    "min": number or null,
    "max": number or null
  }},
  "usage_context": string or null,
  "feature_preferences": [],
  "missing_fields": []
}}

User Query:
{user_query}
"""