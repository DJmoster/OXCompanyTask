DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'job_position') THEN
        CREATE TYPE job_position AS ENUM (
            'Software Engineer',
            'Data Scientist',
            'Human Resources'
        );
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    position job_position NOT NULL
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'auth_role') THEN
        CREATE TYPE auth_role AS ENUM (
            'Admin',
            'Moderator',
            'User'
        );
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS auth (
    id SERIAL PRIMARY KEY,
    role auth_role NOT NULL,
    password BYTEA NOT NULL,
    is_active BOOLEAN NOT NULL,
    employee_id INT UNIQUE NOT NULL,

    FOREIGN KEY (employee_id) REFERENCES employees(id)
        ON DELETE CASCADE
);