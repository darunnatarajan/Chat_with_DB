import pandas as pd

def format_results(headers, rows):
    df = pd.DataFrame(rows, columns=headers)
    return df.to_markdown(index=False, tablefmt="github")
