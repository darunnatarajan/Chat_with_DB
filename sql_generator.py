import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

def clean_sql_output(sql: str) -> str:
    # Removes Markdown-style code blocks (e.g., ```sql) and trims whitespace
    return re.sub(r"```(?:sql)?\n?|```", "", sql).strip()

def generate_sql_from_prompt(prompt):
    endpoint = "https://api.groq.com/openai/v1/chat/completions"
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a MySQL SQL expert. Convert the prompt to a syntactically correct MySQL query "
                    "using the provided schema only. Avoid UNION between SELECTs that return a different number of columns. "
                    "Do not use SELECT * inside UNIONs. Explicitly specify the same columns and types in each SELECT. "
                    "If querying multiple date fields from different tables, return each in a separate SELECT block or alias them uniformly. "
                    "Always return a valid SELECT statement, and never guess unknown table or column names."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }

    print("📤 Sending prompt to Groq:\n", prompt)
    response = requests.post(endpoint, headers=headers, json=payload)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("❌ Error response:", response.text)
        raise e

    raw_sql = response.json()["choices"][0]["message"]["content"]
    cleaned_sql = clean_sql_output(raw_sql)

    # Empty or invalid SQL check
    if not cleaned_sql.strip():
        raise ValueError("⚠️ No SQL generated. Check your prompt or model response.")

    if "SELECT" not in cleaned_sql.upper():
        raise ValueError("⚠️ Generated output doesn't contain a valid SQL SELECT statement.")

    # Validate UNION compatibility
    if "UNION" in cleaned_sql.upper():
        selects = [s.strip() for s in cleaned_sql.upper().split("UNION")]
        column_counts = [s.count(",") + 1 for s in selects]
        if len(set(column_counts)) != 1:
            raise ValueError("⚠️ The generated SQL has UNIONs with mismatched column counts. Please refine your query.")

        if "*" in cleaned_sql:
            raise ValueError("⚠️ Detected SELECT * used in UNIONs. This leads to mismatched columns. Please avoid SELECT * in UNIONs.")

    return cleaned_sql
