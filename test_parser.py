# test_parser.py

from parser_agent.parser import ParserAgent

agent = ParserAgent()
query = "Show names and salaries of employees in engineering earning more than 50000"
parsed = agent.parse(query)
print(parsed)