def classify_intent(parsed_data: dict) -> str:
    verbs = parsed_data.get("verbs", [])
    if not verbs:
        action = parsed_data.get("action")
        if action:
            verbs = [action]
    nouns = parsed_data.get("nouns", [])
    
    # Normalize
    verb_set = set(verb.lower() for verb in verbs)
    noun_set = set(noun.lower() for noun in nouns)

    if any(verb in verb_set for verb in ["add", "insert", "create"]):
        return "INSERT"
    
    if any(verb in verb_set for verb in ["update", "modify", "change", "set"]):
        return "UPDATE"
    
    if any(verb in verb_set for verb in ["delete", "remove", "drop"]):
        return "DELETE"

    if any(verb in verb_set for verb in ["show", "get", "list", "display", "give", "select"]):
        if any(word in noun_set for word in ["total", "average", "sum", "count", "max", "min", "group"]):
            return "AGGREGATE"
        return "SELECT"

    if parsed_data.get("action") == "aggregate":
        return "AGGREGATE"

    if parsed_data.get("function") in ["avg", "sum", "count"]:
        return "AGGREGATE"
    
    if parsed_data.get("action") == "aggregate":
        return "AGGREGATE"
    return "SELECT"

if __name__ == "__main__":
    sample_input = {
        "tokens": ["Show", "me", "the", "average", "salary", "by", "department"],
        "nouns": ["the average salary", "department"],
        "verbs": ["show"]
    }

    intent = classify_intent(sample_input)
    print(f"Intent: {intent}")