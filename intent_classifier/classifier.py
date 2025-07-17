def classify_intent(parsed_data: dict) -> str:
    verbs = parsed_data.get("verbs", [])
    nouns = parsed_data.get("nouns", [])
    
    # Define rules
    verb_set = set(verb.lower() for verb in verbs)

    if any(verb in verb_set for verb in ["show", "get", "list", "display", "give"]):
        if any(word in "total average sum count max min group".split() for word in nouns):
            return "AGGREGATE"
        return "SELECT"

    if any(verb in verb_set for verb in ["add", "insert", "create"]):
        return "INSERT"
    
    if any(verb in verb_set for verb in ["update", "modify", "change"]):
        return "UPDATE"
    
    if any(verb in verb_set for verb in ["delete", "remove", "drop"]):
        return "DELETE"
    
    return "UNKNOWN"

if __name__ == "__main__":
    sample_input = {
        "tokens": ["Show", "me", "the", "average", "salary", "by", "department"],
        "nouns": ["the average salary", "department"],
        "verbs": ["show"]
    }

    intent = classify_intent(sample_input)
    print(f"Intent: {intent}")