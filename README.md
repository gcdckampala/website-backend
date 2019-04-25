# Google Cloud Developer Community Kampala Backend API

## Product Description

## Development set up

#### Set up 

- Check that python 3, pip, virtualenv and postgres are installed

- Clone the GCDC API repo and cd into it
    ```
    git clone https://github.com/gcdckampala/website-backend.git
    ```
- Create virtual env
    ```
    virtualenv --python=python3 venv
    ```
- Activate virtual env
    ```
    source venv/bin/activate
    ```
- Install dependencies
    ```
    pip install -r requirements.txt
    ```
- Create Application environment variables and save them in .env-sample file
    ```
   SECRET = 'Secret Key'
   FLASK_ENV = 'development'
   PORT = 5000
   DATABASE_URL_PROD = "postgresql://{DB_HOST}/{DB_NAME}?user={DB_USER}&password={DB_PASSWORD}"
   DATABASE_URL_DEV = "postgresql://{DB_HOST}/{DB_NAME}?user={DB_USER}&password={DB_PASSWORD}"
   DATABASE_URL_TEST = "postgresql://{DB_HOST}/{DB_NAME}?user={DB_USER}&password={DB_PASSWORD}"

    ```
- Running migrations
    - create a migration file
        ```
        python manage.py db migrate -m "Migration Message"
        ```
    - Apply Migrations
        ```
        python manage.py db upgrade
        ```

- Run application.
    ```
    python manage.py runserver
    ```

- Running Tests
     - To run tests, run the command below.
        ```
        python manage.py test
        ```
    - To run  and check for test coverage. Run the command below:
        ```
        python manage.py test_coverage
        ```
 

## Built with
- Python version  3
- Flask
- Postgres

## Contribution guide
##### Contributing
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.This Project shall be utilising a [GitHub Issues](https://github.com/gcdckampala/website-backend/issues) to track  the work done.

 ##### Pull Request Process
- A contributor shall identify a task to be done from the [GitHub Issues](https://github.com/gcdckampala/website-backend/issues) .If there is a bug , feature or chore that has not be included among the tasks, the contributor can add it only after consulting the owner of this repository and the task being accepted.
- The Contributor shall then create a branch off  the ` develop` branch where they are expected to undertake the task they have chosen.
- After  undertaking the task, a fully detailed pull request shall be submitted to the owners of this repository for review.
- If there any changes requested, it is expected that these changes shall be effected and the pull request resubmitted for review. Once all the changes are accepted, the pull request shall be closed and the changes merged into `develop` by the owners of this repository.
