# brickchain
Brickchain is a platform for the sale and resale of tokens representing fractions of real-world properties.

## Project Structure

The project's folder structure is as follows:

- `app`: Contains the main code of the application.
- `config`: Project configuration files.
- `database`: Contains database files (must not to be uploaded to GitHub).
- `opt`: Contains access credentials (must not be uploaded to GitHub).
- `venv`: Python virtual environment (should not be uploaded to GitHub).
- `.env`: Environment configuration file (should not be uploaded to GitHub).
- `.gitignore`: Files and folders to ignore in Git.
- `docker-compose.yml`: Configuration for Docker Compose.
- `Dockerfile`: Configuration file to build the Docker image.
- `manage.py`: Script to manage the Django project.
- `requirements.txt`: File that lists the dependencies of the project.

## Deploy

### Option 1: Using Docker

To get the system up with Docker, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Taniabarron/brickchain.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd brickchain
    ```

3. **Build the image and lift the containers**:

    ```bash
    docker-compose up --build
    ```

4. **Create a new administrator user**:

    ```bash
    docker-compose exec web sh
    python manage.py createsuperuser
    ```

5. **Applying migrations**:

    ```bash
    docker-compose exec web sh
    python manage.py makemigrations
    python manage.py showmigrations
    python manage.py migrate
    ```
6. **Command for single module migrations** (if necessary):

    ```bash
    docker-compose exec web sh
    python manage.py makemigrations marketplace
    python manage.py migrate
    ```

## Smart Contract
Check the next link: https://github.com/Taniabarron/brickchain-sc
