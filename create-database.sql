CREATE DATABASE roadrunner;

CREATE USER roadrunner_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE roadrunner TO roadrunner_admin;