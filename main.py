#!/usr/bin/env python3
"""
Secure Document Management System (SDMS)
Main entry point for the application
"""

from cli import CLI


def main():
    """Main function to start the SDMS application"""
    print("Initializing Secure Document Management System...")

    # Create and run CLI interface
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()