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

if __name__ == "__main__":
    unittest.main()