def generate_sql(intent: str, tables: list[str], columns: list[str], filters: dict = None) -> str:
    if not tables:
        raise ValueError("No table specified for SQL query.")

    table = tables[0]  # For now, pick the first matched table

    if intent == "SELECT":
        col_clause = ", ".join(columns) if columns else "*"
        if not columns:
            columns = ["*"]
        col_clause = ", ".join(columns)
        sql = f"SELECT {col_clause} FROM {table}"
    elif intent == "AGGREGATE":
        # Assume simple SUM as example
        if not columns:
            columns = ["*"]
        col_clause = ", ".join(columns)
        sql = f"SELECT SUM({col_clause}) FROM {table}"
    elif intent == "INSERT":
        sql = f"-- INSERT INTO {table} (...) VALUES (...);"
    elif intent == "UPDATE":
        sql = f"-- UPDATE {table} SET ... WHERE ...;"
    elif intent == "DELETE":
        sql = f"DELETE FROM {table}"
    else:
        sql = "-- Unknown intent"

    if filters and intent in ["SELECT", "AGGREGATE"]:
        where_clauses = []
        for key, condition in filters.items():
            if isinstance(condition, dict):
                for op, val in condition.items():
                    op_map = {"gt": ">", "lt": "<", "eq": "="}
                    operator = op_map.get(op, "=")
                    if isinstance(val, str):
                        where_clauses.append(f"{key} {operator} '{val}'")
                    else:
                        where_clauses.append(f"{key} {operator} {val}")
            else:
                if isinstance(condition, str):
                    where_clauses.append(f"{key} = '{condition}'")
                else:
                    where_clauses.append(f"{key} = {condition}")

        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

    return sql + ";"

if __name__ == "__main__":
    intent = "SELECT"
    tables = ["employees"]
    columns = ["name", "salary"]
    filters = {"salary": {"gt": 50000}, "department": "engineering"}

    query = generate_sql(intent, tables, columns, filters)
    print(query)