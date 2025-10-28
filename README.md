# SwaB Asset Management System

This project connects to a Google Cloud SQL (MySQL) database using Python, the Google Cloud SQL Connector, and SQLAlchemy.

1. Project Setup  
A. Clone the Repository  
First, clone this repository to your local machine:

```
git clone <your-repository-url>
cd <your-repository-directory>
```

B. Create a Python Virtual Environment  
It is highly recommended to use a virtual environment to manage project dependencies.

# Create the virtual environment
```
python3 -m venv venv
```

# Activate the environment
### On macOS/Linux:
```
source venv/bin/activate
```

### On Windows (Command Prompt):
```
venv\Scripts\activate
```

C. Install Dependencies  
Install the required Python libraries using the requirements.txt file.

```
pip install -r requirements.txt
```

D. Configure Credentials  
This project uses a config.ini file to manage database credentials.  
Copy the example: cp config.ini.example config.ini (If you have an example file).  
Edit config.ini: Open the config.ini file and fill in the correct values provided by your project admin:

```
[mysql]
db_user = YOUR_DB_USER
db_password = YOUR_DB_PASSWORD
db_name = YOUR_DB_NAME
instance_connection_name = my-project:region:my-instance
```

2. Google Cloud (gcloud) Setup (Crucial Step)  
This application uses the Google Cloud SQL Connector library, which automatically handles secure connections (IAM authorization, encryption, etc.).  
To use it, you must authenticate your local machine using the gcloud command-line tool.

A. Install the Google Cloud SDK  
You need to install the gcloud CLI.  
Official Guide: Follow the instructions for your operating system:
https://cloud.google.com/sdk/docs/install

B. Initialize and Authenticate gcloud  
This is the most important step. This command will open a web browser, ask you to log in to your Google account, and grant the SDK permissions to access Google Cloud services on your behalf.

Run the following command in your terminal:

```
gcloud auth application-default login
```

A browser window will open.  
Log in with your company Google account (the one that has access to the Google Cloud project).  
Approve the permissions request.  
This command creates a local credential file that the Python connector library (db.py) will automatically find and use to authenticate.

C. Verify IAM Permissions  
To connect to the database, your Google account must have the "Cloud SQL Client" IAM role on the project.  
If you see a 403 Forbidden or "access denied" error when running the app, it's almost certainly because your account is missing this role. Please contact your project administrator to have it added.

3. Run the Application  
Once you have:

Installed dependencies (`pip install -r requirements.txt`)

Filled in config.ini  
Authenticated with gcloud auth application-default login  
...you are ready to run the application:

```
python main.py
```

You should see output in your terminal indicating a successful connection, table setup, and data fetching.