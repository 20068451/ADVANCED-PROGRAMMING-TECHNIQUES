CREATE DATABASE OnboardingDB;
GO

USE OnboardingDB;
GO

IF OBJECT_ID('users', 'U') IS NOT NULL
    DROP TABLE users;
GO

CREATE TABLE users (
    user_id        INT IDENTITY(1,1) PRIMARY KEY,
    username       VARCHAR(50) NOT NULL UNIQUE,
    password_hash  VARCHAR(64) NOT NULL
);
GO

INSERT INTO users (username, password_hash)
VALUES (
    'hradmin',
    'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
);
GO

IF OBJECT_ID('employees', 'U') IS NOT NULL
    DROP TABLE employees;
GO

CREATE TABLE employees (
    employee_id     VARCHAR(20) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    date_of_joining DATE NOT NULL,
    address         VARCHAR(200) NOT NULL,
    ppsn            VARCHAR(9)  NOT NULL,
    position        VARCHAR(100) NOT NULL,
    department      VARCHAR(50) NOT NULL,
    status          VARCHAR(20) NOT NULL
);
GO

IF OBJECT_ID('assets', 'U') IS NOT NULL
    DROP TABLE assets;
GO

CREATE TABLE assets (
    asset_id    INT IDENTITY(1,1) PRIMARY KEY,
    asset_name  VARCHAR(100) NOT NULL,
    asset_type  VARCHAR(20) NOT NULL,
    status      VARCHAR(20) NOT NULL,
    assigned_to VARCHAR(20) NULL
        REFERENCES employees(employee_id)
);
GO

IF OBJECT_ID('activity_log', 'U') IS NOT NULL
    DROP TABLE activity_log;
GO

CREATE TABLE activity_log (
    log_id        INT IDENTITY(1,1) PRIMARY KEY,
    employee_id   VARCHAR(20) NOT NULL,
    activity_type VARCHAR(20) NOT NULL,
    department    VARCHAR(50) NOT NULL,
    activity_time DATETIME NOT NULL DEFAULT(GETDATE()),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
GO

INSERT INTO employees (employee_id, name, date_of_joining, address, ppsn, position, department, status)
VALUES
('2000-001', 'Alice Johnson',   '2024-01-10', '12 Green Park, Dublin',    '111111111', 'Software Engineer',   'IT',         'ACTIVE'),
('2000-002', 'Brian O''Connor', '2024-01-12', '44 Oak Lane, Dublin',      '222222222', 'DevOps Engineer',     'IT',         'ACTIVE'),
('2000-003', 'Catherine Hill',  '2024-01-20', '22 Willow Street, Dublin', '333333333', 'QA Engineer',         'IT',         'ACTIVE');
GO

INSERT INTO assets (asset_name, asset_type, status, assigned_to) VALUES
('Laptop-001', 'Laptop', 'Assigned',  '2000-001'),
('Laptop-002', 'Laptop', 'Assigned',  '2000-002'),
('Laptop-003', 'Laptop', 'Available', NULL),
('Phone-001',  'Phone',  'Available', NULL),
('Phone-002',  'Phone',  'Available', NULL);
GO

INSERT INTO activity_log (employee_id, activity_type, department, activity_time)
SELECT employee_id, 'ONBOARD', department, date_of_joining
FROM employees;
GO
