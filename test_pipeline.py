import unittest
from pipeline import nl_to_sql

class TestNaturalSQLPipeline(unittest.TestCase):

    def test_salary_query(self):
        query = "List the salaries and names of employees in engineering who earn more than 50000"
        expected_keywords = ["SELECT", "salary", "name", "FROM employees", "WHERE", "salary > 50000", "department = 'engineering'"]

        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_simple_name_query(self):
        query = "Show names of employees"
        expected_keywords = ["SELECT", "name", "FROM employees"]

        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_aggregate_query(self):
        query = "What is the average salary in employees?"
        expected_keywords = ["SELECT", "AVG(salary)", "FROM employees"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_insert_query(self):
        query = "Insert a new employee named John with salary 60000"
        expected_keywords = ["INSERT INTO employees", "John", "60000"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_update_query(self):
        query = "Update salary to 75000 for employees in marketing"
        expected_keywords = ["UPDATE employees", "SET salary = 75000", "WHERE department = 'marketing'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_delete_query(self):
        query = "Delete employees with salary less than 30000"
        expected_keywords = ["DELETE FROM employees", "WHERE", "salary < 30000"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_delete_department_query(self):
        query = "Delete all employees in sales department"
        expected_keywords = ["DELETE FROM employees", "WHERE", "department = 'sales'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_complex_where_conditions(self):
        query = "Show employees who earn between 40000 and 80000"
        expected_keywords = ["SELECT", "FROM employees", "WHERE"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_count_aggregate(self):
        query = "Count the number of employees"
        expected_keywords = ["SELECT", "COUNT", "FROM employees"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_sum_aggregate(self):
        query = "What is the total salary of all employees"
        expected_keywords = ["SELECT", "SUM", "FROM employees"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_multiple_columns_select(self):
        query = "Show employee names, salaries, and departments"
        expected_keywords = ["SELECT", "name", "salary", "FROM employees"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_insert_with_department(self):
        query = "Insert a new employee named Alice with salary 55000 in engineering"
        expected_keywords = ["INSERT INTO employees", "Alice", "55000"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_update_multiple_conditions(self):
        query = "Update salary to 65000 for employees in engineering who earn less than 50000"
        expected_keywords = ["UPDATE employees", "SET salary = 65000", "WHERE"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_select_with_ordering(self):
        query = "Show employees ordered by salary"
        expected_keywords = ["SELECT", "FROM employees"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_case_insensitive_query(self):
        query = "SHOW ALL EMPLOYEES"
        expected_keywords = ["SELECT", "FROM employees"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_empty_query(self):
        query = ""
        sql = nl_to_sql(query)
        self.assertIsInstance(sql, str)

    def test_whitespace_only_query(self):
        query = "   "
        sql = nl_to_sql(query)
        self.assertIsInstance(sql, str)

    def test_age_filters(self):
        query = "Show employees older than 30"
        expected_keywords = ["SELECT", "FROM employees", "WHERE", "age > 30"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_age_between_filters(self):
        query = "Show employees with age between 25 and 40"
        expected_keywords = ["SELECT", "FROM employees", "WHERE", "age BETWEEN 25 AND 40"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_city_filters(self):
        query = "Show employees in New York"
        expected_keywords = ["SELECT", "FROM employees", "WHERE", "city = 'New York'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_join_date_filters(self):
        query = "Show employees who joined after 2020-01-01"
        expected_keywords = ["SELECT", "FROM employees", "WHERE", "join_date > '2020-01-01'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_join_year_filters(self):
        query = "Show employees who joined in 2021"
        expected_keywords = ["SELECT", "FROM employees", "WHERE", "join_date LIKE '2021%'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_position_filters(self):
        query = "Show employees with position Software Engineer"
        expected_keywords = ["SELECT", "FROM employees", "WHERE", "position = 'Software Engineer'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_multiple_columns_select(self):
        query = "Show employee names, cities, and ages"
        expected_keywords = ["SELECT", "name", "city", "age", "FROM employees"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_insert_with_multiple_fields(self):
        query = "Insert a new employee named Alice with salary 55000, age 28, from London, as Software Engineer"
        expected_keywords = ["INSERT INTO employees", "Alice", "55000", "28", "London", "Software Engineer"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_insert_with_email(self):
        query = "Insert a new employee named Bob with email bob@company.com and salary 60000"
        expected_keywords = ["INSERT INTO employees", "Bob", "bob@company.com", "60000"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_complex_where_combination(self):
        query = "Show employees in New York who are older than 25 and earn more than 50000"
        expected_keywords = ["SELECT", "FROM employees", "WHERE", "city = 'New York'", "age > 25", "salary > 50000"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_update_age(self):
        query = "Update age to 35 for employees in marketing"
        expected_keywords = ["UPDATE employees", "SET age = 35", "WHERE department = 'marketing'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_delete_by_age(self):
        query = "Delete employees younger than 25"
        expected_keywords = ["DELETE FROM employees", "WHERE", "age < 25"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

    def test_delete_by_city(self):
        query = "Delete all employees in Tokyo"
        expected_keywords = ["DELETE FROM employees", "WHERE", "city = 'Tokyo'"]
        sql = nl_to_sql(query)
        for keyword in expected_keywords:
            self.assertIn(keyword, sql)

if __name__ == "__main__":
    unittest.main()