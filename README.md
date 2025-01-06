# QA Assignment - Supplier Relationship Manager (SRM)

This website application is for the Software Engineering & Agile module of the DTS apprenticeship course. This application is a basic SRM that can collect data for suppliers that could be used by customers within a procurement organisation. Users can register, log in, create, read, and update data entries. Admin users have access to delete functionality too. 

## Prerequisites

Before running this application, ensure you have the following installed:

- Python (version 3.11) test
- pip (Python package installer)
- Git (version control)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/SamB-CCS/srm_project
```

2. Navigate to the project directory:
```bash
cd srm_project
```

3. Create a virtual environment (recommended):
```bash
python -m venv env
```

4. Activate the virtual environment:
- On Windows:
```bash
env\Scripts\activate
```
- On Unix or macOS:
```bash
source env/bin/activate
```

5. Next, install the required packages:
```bash
pip install -r requirements.txt
```

6. Apply database migrations:
```bash
python manage.py migrate
```
7. Create a superuser (optional, but recommended for admin access):
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a superuser account.

## Configuration

Before running the application, you may need to configure some settings. Open the `srm_project/settings.py` file and adjust the following variables according to your needs:

- `SECRET_KEY`: Set a secure secret key for your application.
- `DEBUG`: Set to `False` in production environments.
- `ALLOWED_HOSTS`: Add your domain or server IP address.
- `DATABASES`: Configure your database settings.

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```
2. Open your web browser and navigate to `http://localhost:8000` to access the application.

## Running Tests

To run the test suite, use the following command:
```bash
pytest
```
## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Create a pull request, and we'll review your changes.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Python](https://www.python.org/)
- [Pip](https://pypi.org/project/pip/)
