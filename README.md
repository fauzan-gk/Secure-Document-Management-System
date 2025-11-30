# Secure Document Management System

A simple, secure document management system built in Python — enabling encrypted storage, access control, and secure document handling.  

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Security Considerations](#security-considerations)  
- [Contributing](#contributing)  
- [License](#license)  

## Features

- Document upload/download with encryption/decryption.  
- User authentication & access control.  
- CLI-based interface (command-line) to manage documents.  
- Simple local database (SQLite) to store metadata.  
- Organized folder structure for uploaded files and download output.  

## Tech Stack

- Language: Python  
- Database: SQLite (via built-in `sqlite3`)  
- Cryptography: Custom module for encryption/decryption  
- CLI support: Python scripts (no GUI)  

## Getting Started

### Prerequisites

- Python 3.x installed  
- `pip` for installing dependencies  

### Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/fauzan-gk/Secure-Document-Management-System.git  
   cd Secure-Document-Management-System

   Usage

### Run the main program:

python main.py


Use the CLI prompts to register/login, upload documents, download documents, or manage stored files.

You can also explore other scripts/modules:

auth.py — handles user authentication.

crypto.py — handles encryption/decryption logic.

document_manager.py — main logic for document upload/download & metadata management.

### Project Structure
/ (root)
├─ auth.py  
├─ crypto.py  
├─ document_manager.py  
├─ cli.py  
├─ main.py  
├─ database.py  
├─ requirements.txt  
├─ sdms.db             # SQLite database file  
├─ uploads/            # user-uploaded encrypted documents  
├─ downloads/          # decrypted/downloaded documents  
├─ __pycache__/  
└─ test_file           # placeholder/test file  


uploads/ — stores encrypted documents.

downloads/ — stores decrypted or user-downloaded documents.

sdms.db — SQLite file with metadata: users, document info, permissions, etc.

Security Considerations

Sensitive data (documents) is encrypted before storage.

Use strong passwords for user accounts.

Do not store plaintext sensitive documents directly in the repo.

Use .gitignore to exclude config files or environment variables (if added later).

⚠️ If you extend this project (e.g. add web interface, multi-user networked use), ensure to properly secure credentials and storage, and consider more robust encryption & authentication flows.

### Contributing

Feel free to open issues or pull requests if you find bugs or want to add features. Ideas for future improvements:

Add a web interface (Flask/Django)

Multi-user / role-based permissions

Support for external storage (cloud, network drive)

Logging, auditing of document access

Unit / integration tests

When contributing:

Fork the project

Create a new branch (feature/your-feature)

Commit changes & open a pull request

### License

This project is open-source. You may add a LICENSE file (e.g., MIT, Apache-2.0) depending on your needs.
