CREATE DATABASE OnboardingDB;
GO

USE OnboardingDB;
GO

IF OBJECT_ID('users', 'U') IS NOT NULL
    DROP TABLE users;
GO

CREATE TABLE users (
    user_id   INT IDENTITY(1,1) PRIMARY KEY,
    username  VARCHAR(50) NOT NULL UNIQUE,
    password  VARCHAR(100) NOT NULL
);
GO

INSERT INTO users (username, password)
VALUES ('hradmin', 'password123');
GO
