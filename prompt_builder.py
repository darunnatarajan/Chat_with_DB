def build_prompt(schema_str, user_question):
    return f"""
You are an expert SQL generator.

Given the following MySQL database schema:

{schema_str}

Generate a syntactically correct SQL query to answer the following natural language question:

"{user_question}"

Only return the SQL query. Do not add explanations.
"""
