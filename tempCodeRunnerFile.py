"""Orchestrates everything: gets schema → builds prompt → generates SQL → runs query → formats result."""

from schema_reader import read_schema
from schema_formatter import format_schema
from prompt_builder import build_prompt
from sql_generator import generate_sql_from_prompt
from query_runner import run_sql_query
from result_formatter import format_results

def main():
    user_input = input("Ask a question in natural language: ")

    schema = read_schema()
    schema_str = format_schema(schema)
    prompt = build_prompt(schema_str, user_input)
    sql = generate_sql_from_prompt(prompt)

    print("\nGenerated SQL Query:\n", sql)

    try:
        headers, rows = run_sql_query(sql)
        formatted = format_results(headers, rows)
        print("\nQuery Result:\n", formatted)
    except Exception as e:
        print("Error running SQL query:", e)

if __name__ == "__main__":
    main()
