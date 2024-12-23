# OXCompanyTask

A backend for the employee management system with the ability to grant authorization access only to selected employees and the ability to control access to endpoints using authorization roles

## Installation

### Creating enviroment
    python -m venv .venv
####
    .venv\Scripts\activate.bat
    

### Dependency install
    pip install -r requirements.txt

### Dependency install using poetry (Optional)
    pip install poetry
####
    poetry install

## Running app

### Manual run
Note: before run application manually you need to create and fill **.env** file. All required fields you can find in **example.env**
    
    uvicorn app.main:app

### Running app via Docker Compose (Optional)
    docker-compose up --build -d

After starting app will create all necessary tables and types in database. \
You can open the app Swagger at this link:
http://localhost:8000/docs \
Default admin user credentials: 
- admin@admin.com
- 1234567890







