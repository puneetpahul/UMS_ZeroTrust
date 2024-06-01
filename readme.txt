Setting Up and Running University Mangement system

1. Install Visual Studio Code (VSCode)
   - Download and install VSCode from here: https://code.visualstudio.com/.

2. Install Python
   - Download and install the latest version of Python from here: https://www.python.org/downloads/.

3. Install Git Bash
   - Download and install Git Bash from here: https://gitforwindows.org/.

4. Integrate Git Bash with VSCode as Default Terminal
   - Open VSCode.
   - Go to File > Preferences > Settings.
   - In the search bar, type terminal.integrated.shell.windows.
   - Click on Edit in settings.json and add the following line:
     "terminal.integrated.shell.windows": "C:\Program Files\Git\bin\bash.exe"

5. Clone the Repository
   - Open Git Bash.
   - Run the command:
     git clone https://github.com/puneetpahul/UMS_ZeroTrust.git

6. Navigate to the Project Directory
   - Change to the project directory:
     cd UMS_ZeroTrust

7. Install Virtualenv
   - Run the command to install virtualenv:
     pip3 install virtualenv

8. Create and Activate Virtual Environment
   - Create the virtual environment:
     virtualenv venv
   - Activate the virtual environment:
     - On Windows:
       source venv/Scripts/activate
     - On macOS/Linux:
       source venv/bin/activate

9. Install Project Dependencies
   - Install the required packages:
     pip install -r requirements.txt

10. Navigate to the Project Subdirectory
    - Change to the ums subdirectory:
      cd ums

11. Apply Migrations
    - Run the following commands to create the necessary database tables:
      python manage.py makemigrations
      python manage.py migrate

12. Create a Superuser
    - Create a superuser to access the Django admin panel:
      python manage.py createsuperuser

13. Run the Development Server
    - Start the Django development server:
      python manage.py runserver 8001

14. Access the Application
    - Open your web browser and navigate to the generated link, typically http://127.0.0.1:8001/.
