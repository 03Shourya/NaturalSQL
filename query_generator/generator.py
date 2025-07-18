def generate_sql(intent: str, tables: list[str], columns: list[str], filters: dict = None) -> str:
    if not tables:
        raise ValueError("No table specified for SQL query.")

    table = tables[0]  # For now, pick the first matched table
    
    # Mapping from schema column names to display names
    display_names = {
        "department_id": "department"
    }

    if intent == "SELECT":
        col_clause = ", ".join(columns) if columns else "*"
        if not columns:
            columns = ["*"]
        col_clause = ", ".join(columns)
        sql = f"SELECT {col_clause} FROM {table}"
        if filters:
            where_clauses = []
            for key, condition in filters.items():
                # Skip function key as it's not a filter condition
                if key == "function":
                    continue
                if isinstance(condition, dict):
                    for op, val in condition.items():
                        op_map = {"gt": ">", "lt": "<", "eq": "="}
                        operator = op_map.get(op, "=")
                        display_key = display_names.get(key, key)
                        if isinstance(val, str):
                            where_clauses.append(f"{display_key} {operator} '{val}'")
                        else:
                            where_clauses.append(f"{display_key} {operator} {val}")
                else:
                    display_key = display_names.get(key, key)
                    if isinstance(condition, str):
                        where_clauses.append(f"{display_key} = '{condition}'")
                    else:
                        where_clauses.append(f"{display_key} = {condition}")

            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
    elif intent == "AGGREGATE":
        func = filters.get("function", "AVG").upper() if filters else "AVG"
        if not columns:
            columns = ["*"]
        col_clause = ", ".join([f"{func}({col})" for col in columns])
        sql = f"SELECT {col_clause} FROM {table}"
        if filters:
            where_clauses = []
            for key, condition in filters.items():
                # Skip function key as it's not a filter condition
                if key == "function":
                    continue
                if isinstance(condition, dict):
                    for op, val in condition.items():
                        op_map = {"gt": ">", "lt": "<", "eq": "="}
                        operator = op_map.get(op, "=")
                        display_key = display_names.get(key, key)
                        if isinstance(val, str):
                            where_clauses.append(f"{display_key} {operator} '{val}'")
                        else:
                            where_clauses.append(f"{display_key} {operator} {val}")
                else:
                    display_key = display_names.get(key, key)
                    if isinstance(condition, str):
                        where_clauses.append(f"{display_key} = '{condition}'")
                    else:
                        where_clauses.append(f"{display_key} = {condition}")

            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
    elif intent == "INSERT":
        if filters:
            cols = ", ".join(filters.keys())
            vals = ", ".join([f"'{v.title()}'" if isinstance(v, str) else str(v) for v in filters.values()])
            sql = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
        else:
            sql = f"INSERT INTO {table} (...) VALUES (...);"
    elif intent == "UPDATE":
        if filters:
            set_parts = []
            where_parts = []
            for key, value in filters.items():
                display_key = display_names.get(key, key)
                if key == "department_id":
                    where_parts.append(f"{display_key} = '{value}'")
                elif key == "salary":
                    # For UPDATE, salary goes in SET clause
                    val_str = f"'{value}'" if isinstance(value, str) else str(value)
                    set_parts.append(f"{key} = {val_str}")
                else:
                    val_str = f"'{value}'" if isinstance(value, str) else str(value)
                    set_parts.append(f"{key} = {val_str}")
            set_clause = "SET " + ", ".join(set_parts) if set_parts else ""
            where_clause = "WHERE " + " AND ".join(where_parts) if where_parts else ""
            sql = f"UPDATE {table} {set_clause} {where_clause}".strip()
        else:
            sql = f"UPDATE {table} SET ... WHERE ...;"
    elif intent == "DELETE":
        sql = f"DELETE FROM {table}"
    else:
        sql = "-- Unknown intent"

    return sql + ";"

if __name__ == "__main__":
    intent = "SELECT"
    tables = ["employees"]
    columns = ["name", "salary"]
    filters = {"salary": {"gt": 50000}, "department": "engineering"}

    query = generate_sql(intent, tables, columns, filters)
    print(query)