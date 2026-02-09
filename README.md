# Voting System

An online voting system built with Flask and Oracle Database that allows registered voters to securely cast their votes in elections.

## Features

- **User Authentication**: Secure registration and login system for voters
- **Voting Interface**: Easy-to-use interface for casting votes
- **Admin Panel**: Administrative features for managing candidates
- **Candidate Management**: Add, edit, and delete candidate information with images
- **Results Display**: View real-time voting results
- **One Vote Per User**: Ensures each registered voter can only vote once
- **Secure & Transparent**: Built with security and transparency in mind

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: Oracle Database (cx_Oracle)
- **Frontend**: HTML, CSS, JavaScript
- **Template Engine**: Jinja2

## Installation

### Prerequisites

- Python 3.11+
- Oracle Database (XE or higher)
- Oracle Instant Client (64-bit)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/SanthoshRamesh007/Voting_System.git
   cd Voting_System
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Oracle Database**
   - Ensure Oracle Database service is running
   - Update database credentials in `app.py` and `database.py`
   - Start the Oracle TNS Listener

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
Dbms_Project/
├── app.py                      # Main Flask application
├── database.py                 # Database connection utilities
├── requirements.txt            # Python dependencies
├── voting_system.db           # SQLite database file
├── static/
│   └── candidate_images/      # Candidate profile images
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Homepage
    ├── login.html             # Login page
    ├── register.html          # Voter registration
    ├── vote.html              # Voting interface
    ├── results.html           # Results display
    ├── candidate_register.html # Add new candidate
    ├── edit_candidate.html    # Edit candidate details
    └── manage_candidates.html # Manage all candidates
```

## Usage

### For Voters
1. Register as a new voter with your details
2. Login with your credentials
3. Navigate to the "Vote" page
4. Select your preferred candidate
5. Submit your vote

### For Administrators
1. Login with admin credentials
2. Access "Manage Candidates" to add/edit/delete candidates
3. Upload candidate images
4. View voting results

## Database Configuration

Update the database connection settings in `app.py`:

```python
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
connection = cx_Oracle.connect(user="system", password="your_password", dsn=dsn)
```

## Security Features

- Password authentication for voters
- Admin role-based access control
- Session management
- One-vote-per-voter enforcement

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Author

Santhosh Ramesh

## Contact

GitHub: [@SanthoshRamesh007](https://github.com/SanthoshRamesh007)
