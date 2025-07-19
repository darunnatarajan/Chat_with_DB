def format_schema(schema_dict):
    formatted = []
    for table, columns in schema_dict.items():
        column_str = ", ".join(columns)
        formatted.append(f"Table `{table}`: {column_str}")
    return "\n".join(formatted)
