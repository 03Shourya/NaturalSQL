import difflib
from schema_mapper.schema import SCHEMA

def map_to_schema(nouns: list[str]) -> dict:
    mapped = {"tables": set(), "columns": set()}

    all_tables = list(SCHEMA.keys())
    all_columns = sum(SCHEMA.values(), [])

    for noun in nouns:
        noun = noun.lower()
        table_match = difflib.get_close_matches(noun, all_tables, n=1, cutoff=0.6)
        col_match = difflib.get_close_matches(noun, all_columns, n=2, cutoff=0.6)

        if table_match:
            mapped["tables"].add(table_match[0])
        if col_match:
            mapped["columns"].update(col_match)

    # Convert sets to lists
    mapped["tables"] = list(mapped["tables"])
    mapped["columns"] = list(mapped["columns"])
    return mapped

if __name__ == "__main__":
    nouns = ["employee", "salary", "department"]
    print(map_to_schema(nouns))