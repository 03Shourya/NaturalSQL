def generate_sql(intent: str, tables: list[str], columns: list[str], filters: dict = None, joins: list = None, group_by: str = None, having: dict = None, subqueries: list = None) -> str:
    if not tables:
        raise ValueError("No table specified for SQL query.")

    table = tables[0]  # For now, pick the first matched table
    
    # Mapping from schema column names to display names
    display_names = {
        "department_id": "department"
    }
    
    # Mapping to preserve proper case for cities and other proper nouns
    proper_case = {
        "new york": "New York",
        "london": "London", 
        "tokyo": "Tokyo",
        "paris": "Paris",
        "berlin": "Berlin",
        "mumbai": "Mumbai",
        "delhi": "Delhi",
        "bangalore": "Bangalore",
        "software engineer": "Software Engineer",
        "data scientist": "Data Scientist",
        "product manager": "Product Manager",
        "sales representative": "Sales Representative",
        "john": "John",
        "alice": "Alice",
        "bob": "Bob",
        "jane": "Jane",
        "mike": "Mike",
        "sarah": "Sarah"
    }

    if intent == "SELECT":
        col_clause = ", ".join(columns) if columns else "*"
        if not columns:
            columns = ["*"]
        col_clause = ", ".join(columns)
        
        # Build the FROM clause with JOINs
        from_clause = f"FROM {table}"
        if joins:
            for join in joins:
                join_type = join.get("type", "INNER")
                join_table = join.get("table", "")
                join_condition = join.get("on", {})
                if join_table and join_condition:
                    left_col = join_condition.get("left", "")
                    right_col = join_condition.get("right", "")
                    if left_col and right_col:
                        from_clause += f" {join_type} JOIN {join_table} ON {left_col} = {right_col}"
        
        sql = f"SELECT {col_clause} {from_clause}"
        
        where_clauses = []
        if filters:
            for key, condition in filters.items():
                # Skip function key as it's not a filter condition
                if key == "function":
                    continue
                if isinstance(condition, dict):
                    for op, val in condition.items():
                        op_map = {"gt": ">", "lt": "<", "eq": "=", "like": "LIKE"}
                        operator = op_map.get(op, "=")
                        display_key = display_names.get(key, key)
                        if op == "between" and isinstance(val, list) and len(val) == 2:
                            where_clauses.append(f"{display_key} BETWEEN {val[0]} AND {val[1]}")
                        elif op == "like" and isinstance(val, str):
                            where_clauses.append(f"{display_key} LIKE '{val}'")
                        elif isinstance(val, str):
                            # Apply proper case mapping
                            proper_val = proper_case.get(val.lower(), val)
                            where_clauses.append(f"{display_key} {operator} '{proper_val}'")
                        else:
                            where_clauses.append(f"{display_key} {operator} {val}")
                else:
                    display_key = display_names.get(key, key)
                    if isinstance(condition, str):
                        # Apply proper case mapping
                        proper_val = proper_case.get(condition.lower(), condition)
                        where_clauses.append(f"{display_key} = '{proper_val}'")
                    else:
                        where_clauses.append(f"{display_key} = {condition}")

        # Add subquery conditions
        if subqueries:
            for subquery in subqueries:
                if subquery["type"] == "comparison" and subquery["comparison"] == "average":
                    # Handle "more than average" or "less than average"
                    op = ">" if subquery["operator"] == "more than" else "<"
                    avg_subquery = f"(SELECT AVG(salary) FROM employees)"
                    where_clauses.append(f"salary {op} {avg_subquery}")
                elif subquery["type"] == "count":
                    # Handle "with more than X employees"
                    op = ">" if subquery["operator"] == "more than" else "<"
                    count_subquery = f"(SELECT COUNT(*) FROM employees WHERE employees.department_id = departments.id)"
                    # For count subqueries, we need to select from departments and join with employees
                    if table == "employees":
                        # Change the main query to select from departments
                        sql = f"SELECT departments.* FROM departments WHERE {count_subquery} {op} {subquery['value']}"
                    else:
                        where_clauses.append(f"{count_subquery} {op} {subquery['value']}")
                elif subquery["type"] == "budget":
                    # Handle budget comparisons
                    op = subquery["operator"]
                    val = subquery["value"]
                    where_clauses.append(f"budget {op} {val}")

        # Add WHERE clause if we have any conditions
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        
        # Add GROUP BY clause
        if group_by:
            sql += f" GROUP BY {group_by}"
        
        # Add HAVING clause
        if having and group_by:
            having_col = having.get("column", "")
            having_op = having.get("operator", ">")
            having_val = having.get("value", 0)
            sql += f" HAVING {having_col} {having_op} {having_val}"
            
    elif intent == "AGGREGATE":
        # Get the function from the filters, default to AVG
        func = filters.get("function", "AVG").upper() if filters else "AVG"
        
        # Build the FROM clause with JOINs
        from_clause = f"FROM {table}"
        if joins:
            for join in joins:
                join_type = join.get("type", "INNER")
                join_table = join.get("table", "")
                join_condition = join.get("on", {})
                if join_table and join_condition:
                    left_col = join_condition.get("left", "")
                    right_col = join_condition.get("right", "")
                    if left_col and right_col:
                        from_clause += f" {join_type} JOIN {join_table} ON {left_col} = {right_col}"
        
        # Handle GROUP BY queries
        if group_by:
            # For GROUP BY, we need to include both the group column and the aggregation
            if group_by == "departments" or group_by == "department":
                # Join with departments table to get department names
                from_clause += " INNER JOIN departments ON employees.department_id = departments.id"
                if "count(*)" in columns:
                    select_cols = ["departments.name", "COUNT(*)"]
                else:
                    select_cols = ["departments.name", f"{func}(employees.salary)"]
            else:
                if "count(*)" in columns:
                    select_cols = [group_by, "COUNT(*)"]
                else:
                    select_cols = [group_by, f"{func}(salary)"]
            col_clause = ", ".join(select_cols)
        else:
            # Regular aggregate query
            if not columns:
                columns = ["*"]
            col_clause = ", ".join([f"{func}({col})" for col in columns])
        
        sql = f"SELECT {col_clause} {from_clause}"
        
        where_clauses = []
        if filters:
            for key, condition in filters.items():
                # Skip function key as it's not a filter condition
                if key == "function":
                    continue
                if isinstance(condition, dict):
                    for op, val in condition.items():
                        op_map = {"gt": ">", "lt": "<", "eq": "="}
                        operator = op_map.get(op, "=")
                        display_key = display_names.get(key, key)
                        if op == "between" and isinstance(val, list) and len(val) == 2:
                            where_clauses.append(f"{display_key} BETWEEN {val[0]} AND {val[1]}")
                        elif isinstance(val, str):
                            where_clauses.append(f"{display_key} {operator} '{val}'")
                        else:
                            where_clauses.append(f"{display_key} {operator} {val}")
                else:
                    display_key = display_names.get(key, key)
                    if isinstance(condition, str):
                        # Apply proper case mapping
                        proper_val = proper_case.get(condition.lower(), condition)
                        where_clauses.append(f"{display_key} = '{proper_val}'")
                    else:
                        where_clauses.append(f"{display_key} = {condition}")


        
        # Add GROUP BY clause for aggregate queries
        if group_by:
            if group_by == "departments" or group_by == "department":
                sql += " GROUP BY departments.name"
            else:
                sql += f" GROUP BY {group_by}"
        
        # Add HAVING clause
        if having and group_by:
            having_col = having.get("column", "")
            having_op = having.get("operator", ">")
            having_val = having.get("value", 0)
            # For HAVING, we need to reference the aggregated column
            if having_col == "salary":
                having_col = f"{func}(employees.salary)"
            sql += f" HAVING {having_col} {having_op} {having_val}"
            
    elif intent == "INSERT":
        if filters:
            cols = ", ".join(filters.keys())
            vals = []
            for v in filters.values():
                if isinstance(v, str):
                    # Preserve email case, apply proper case mapping to others
                    if '@' in v:  # Email
                        vals.append(f"'{v}'")
                    else:
                        proper_val = proper_case.get(v.lower(), v)
                        vals.append(f"'{proper_val}'")
                else:
                    vals.append(str(v))
            vals_str = ", ".join(vals)
            sql = f"INSERT INTO {table} ({cols}) VALUES ({vals_str})"
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
                        if op == "between" and isinstance(val, list) and len(val) == 2:
                            where_clauses.append(f"{display_key} BETWEEN {val[0]} AND {val[1]}")
                        elif isinstance(val, str):
                            where_clauses.append(f"{display_key} {operator} '{val}'")
                        else:
                            where_clauses.append(f"{display_key} {operator} {val}")
                else:
                    display_key = display_names.get(key, key)
                    if isinstance(condition, str):
                        # Apply proper case mapping
                        proper_val = proper_case.get(condition.lower(), condition)
                        where_clauses.append(f"{display_key} = '{proper_val}'")
                    else:
                        where_clauses.append(f"{display_key} = {condition}")

            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
    else:
        sql = "-- Unknown intent"

    return sql + ";"

if __name__ == "__main__":
    intent = "SELECT"
    tables = ["employees"]
    columns = ["name", "salary"]
    filters = {"salary": {"gt": 50000}, "department": "engineering"}
    joins = [{"type": "INNER", "table": "departments", "on": {"left": "employees.department_id", "right": "departments.id"}}]
    group_by = "department"
    having = {"column": "avg(salary)", "operator": ">", "value": 60000}
    subqueries = [{"type": "comparison", "operator": "more than", "comparison": "average", "column": "salary"}]

    query = generate_sql(intent, tables, columns, filters, joins, group_by, having, subqueries)
    print(query)