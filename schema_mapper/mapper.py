import difflib
from schema_mapper.schema import SCHEMA

normalization_map = {
    "the salaries": "salary",
    "names": "name",
    "department": "department_id"
}

def normalize(term):
    return normalization_map.get(term.lower(), term.lower())

def map_to_schema(nouns: list[str], parsed_data=None) -> dict:
    if parsed_data:
        if "columns" in parsed_data:
            parsed_data["columns"] = [normalize(col) for col in parsed_data["columns"]]
        if "filters" in parsed_data:
            parsed_data["filters"] = {
                normalize(k): v for k, v in parsed_data["filters"].items()
            }
        # Filter out keys in filters that are not in schema columns
        if "filters" in parsed_data:
            valid_columns = set(sum(SCHEMA.values(), []))
            parsed_data["filters"] = {
                k: v for k, v in parsed_data["filters"].items() if k in valid_columns
            }

    mapped = {"tables": set(), "columns": set()}

    all_tables = list(SCHEMA.keys())
    all_columns = sum(SCHEMA.values(), [])

    for noun in nouns:
        noun = normalization_map.get(noun.lower(), noun.lower())
        table_match = difflib.get_close_matches(noun, all_tables, n=1, cutoff=0.6)
        col_match = difflib.get_close_matches(noun, all_columns, n=2, cutoff=0.6)

        if table_match:
            mapped["tables"].add(table_match[0])
        if col_match:
            mapped["columns"].update(col_match)

    # Convert sets to lists
    mapped["tables"] = list(mapped["tables"])
    mapped["columns"] = list(mapped["columns"])

    if hasattr(parsed_data, "get") and parsed_data.get("table") in all_tables:
        mapped["tables"].insert(0, parsed_data["table"])
        mapped["tables"] = list(dict.fromkeys(mapped["tables"]))  # remove duplicates

    # Re-rank tables based on number of matched columns
    table_scores = {table: 0 for table in SCHEMA.keys()}
    for col in mapped["columns"]:
        for table, cols in SCHEMA.items():
            if col in cols:
                table_scores[table] += 1

    # Bonus if parser specifies the table
    if hasattr(parsed_data, "get") and parsed_data.get("table") in table_scores:
        table_scores[parsed_data.get("table")] += 2

    sorted_tables = sorted(table_scores.items(), key=lambda x: -x[1])
    mapped["tables"] = [t[0] for t in sorted_tables]

    return mapped

if __name__ == "__main__":
    nouns = ["employee", "salary", "department"]
    print(map_to_schema(nouns))