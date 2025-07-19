from parser_agent.parser import parse_natural_language
from intent_classifier.classifier import classify_intent
from schema_mapper.mapper import map_to_schema
from query_generator.generator import generate_sql

def nl_to_sql(query: str) -> str:
    print(f"\n🔍 Input Query: {query}")

    # Step 1: Parse the query
    parsed = parse_natural_language(query)
    print(f"🧠 Parsed Output: {parsed}")

    # Step 2: Classify intent
    intent = classify_intent(parsed)
    print(f"🎯 Intent Detected: {intent}")

    # Step 3: Map to schema
    nouns = parsed.get("columns", []) + list(parsed.get("filters", {}).keys())
    schema = map_to_schema(nouns, parsed)
    print(f"🗂️ Schema Mapping: {schema}")

    # Step 4: Construct SQL
    # Pass both filters and function information
    filters = parsed.get("filters", {})
    if "function" in parsed:
        filters["function"] = parsed["function"]
    
    # Pass joins information
    joins = parsed.get("joins", [])
    
    # Pass group_by and having information
    group_by = parsed.get("group_by")
    having = parsed.get("having", {})
    
    sql = generate_sql(intent, schema["tables"], schema["columns"], filters, joins, group_by, having)
    print(f"💡 Generated SQL: {sql}")

    return sql

if __name__ == "__main__":
    sample_query = "Show departments with average salary > 50000"
    nl_to_sql(sample_query)