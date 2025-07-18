import sys
import readline
import argparse
from colorama import init, Fore, Style
from pipeline import nl_to_sql

# Initialize colorama for cross-platform colored output
init()

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    """Print text with color and style."""
    print(f"{color}{style}{text}{Style.RESET_ALL}")

def print_help():
    """Display help information."""
    help_text = """
NaturalSQL CLI - Natural Language to SQL Converter

Usage:
  Enter natural language queries and get SQL output
  Type 'help' for this message
  Type 'exit' or 'quit' to exit
  Type 'clear' to clear the screen

Examples:
  - "Show all employees"
  - "List employees in engineering department"
  - "What is the average salary?"
  - "Insert a new employee named John with salary 50000"
  - "Update salary to 60000 for employees in marketing"
  - "Delete employees with salary less than 30000"

Commands:
  help     - Show this help message
  clear    - Clear the screen
  exit     - Exit the application
  quit     - Exit the application
"""
    print_colored(help_text, Fore.CYAN)

def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Set up command history
    history_file = ".naturalsql_history"
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass
    
    # Set up readline for better input experience
    readline.set_history_length(1000)
    
    print_colored("🚀 Welcome to NaturalSQL CLI!", Fore.GREEN, Style.BRIGHT)
    print_colored("Type 'help' for usage instructions, 'exit' to quit.\n", Fore.YELLOW)
    
    while True:
        try:
            # Get user input with colored prompt
            query = input(f"{Fore.BLUE}❯ {Style.RESET_ALL}")
            
            # Handle commands
            if query.strip().lower() in ("exit", "quit"):
                print_colored("👋 Goodbye!", Fore.GREEN)
                break
            elif query.strip().lower() == "help":
                print_help()
                continue
            elif query.strip().lower() == "clear":
                clear_screen()
                print_colored("🚀 Welcome to NaturalSQL CLI!", Fore.GREEN, Style.BRIGHT)
                continue
            elif not query.strip():
                continue
            
            # Process the query
            print_colored("🔄 Processing...", Fore.YELLOW)
            sql = nl_to_sql(query)
            
            # Display results with color
            print_colored("\n📝 Generated SQL:", Fore.GREEN, Style.BRIGHT)
            print_colored(f"{sql}\n", Fore.WHITE, Style.BRIGHT)
            
        except KeyboardInterrupt:
            print_colored("\n👋 Goodbye!", Fore.GREEN)
            break
        except Exception as e:
            print_colored(f"❌ Error: {str(e)}", Fore.RED)
    
    # Save command history
    try:
        readline.write_history_file(history_file)
    except:
        pass

if __name__ == "__main__":
    main() 