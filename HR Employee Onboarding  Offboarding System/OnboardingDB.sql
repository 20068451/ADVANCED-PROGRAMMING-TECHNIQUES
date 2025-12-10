CREATE DATABASE OnboardingDB;
GO
USE OnboardingDB;
GO

CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash NVARCHAR(64) NOT NULL
);

CREATE TABLE employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    date_of_joining DATE NOT NULL,
    address NVARCHAR(255) NOT NULL,
    ppsn CHAR(9) NOT NULL,
    position NVARCHAR(50) NOT NULL,
    department NVARCHAR(50) NOT NULL,
    status NVARCHAR(20) NOT NULL
);

CREATE TABLE assets (
    asset_id INT IDENTITY(1,1) PRIMARY KEY,
    asset_name NVARCHAR(100) NOT NULL,
    asset_type NVARCHAR(20) NOT NULL,
    status NVARCHAR(20) NOT NULL,
    assigned_to VARCHAR(10) NULL
        REFERENCES employees(employee_id)
);

CREATE TABLE activity_log (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    employee_id VARCHAR(10) NOT NULL
        REFERENCES employees(employee_id),
    activity_type NVARCHAR(20) NOT NULL,
    department NVARCHAR(50) NOT NULL,
    activity_time DATETIME NOT NULL DEFAULT(GETDATE())
);

INSERT INTO users (username, password_hash)
VALUES (
    'hradmin',
    'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
);

INSERT INTO employees (employee_id, name, date_of_joining, address, ppsn, position, department, status) VALUES
('2000-001','Alice Johnson','2025-01-05','Dublin 1','123456781','Software Engineer','IT','ACTIVE'),
('2000-002','Brian Miller','2025-01-10','Dublin 2','123456782','QA Engineer','IT','ACTIVE'),
('2000-003','Carol Smith','2025-01-12','Dublin 3','123456783','Team Lead','IT','ACTIVE'),
('2000-004','David Brown','2025-01-15','Dublin 4','123456784','HR Specialist','HR','ACTIVE'),
('2000-005','Emma Davis','2025-01-18','Dublin 5','123456785','Recruiter','HR','ACTIVE'),
('2000-006','Frank Wilson','2025-01-20','Dublin 6','123456786','Accountant','Finance','ACTIVE'),
('2000-007','Grace Lee','2025-01-25','Dublin 7','123456787','Finance Analyst','Finance','ACTIVE'),
('2000-008','Henry Clark','2025-01-28','Dublin 8','123456788','Operations Manager','Operations','ACTIVE'),
('2000-009','Ivy Walker','2025-02-01','Dublin 9','123456789','Support Engineer','IT','ACTIVE'),
('2000-010','Jake Turner','2025-02-03','Dublin 10','223456789','DevOps Engineer','IT','ACTIVE');

INSERT INTO assets (asset_name, asset_type, status, assigned_to) VALUES
('MacBook Pro 14','Laptop','Assigned','2000-001'),
('MacBook Pro 14','Laptop','Assigned','2000-002'),
('Lenovo ThinkPad X1','Laptop','Assigned','2000-003'),
('MacBook Pro 14','Laptop','Assigned','2000-004'),
('MacBook Pro 14','Laptop','Assigned','2000-005'),
('MacBook Pro 14','Laptop','Assigned','2000-006'),
('Lenovo ThinkPad X1','Laptop','Assigned','2000-007'),
('MacBook Air 13','Laptop','Assigned','2000-008'),
('Lenovo ThinkPad X1','Laptop','Assigned','2000-009'),
('Lenovo ThinkPad X1','Laptop','Assigned','2000-010'),
('Lenovo ThinkPad X1','Laptop','Available',NULL),
('Lenovo ThinkPad X1','Laptop','Available',NULL),
('Lenovo ThinkPad X1','Laptop','Available',NULL),
('Lenovo ThinkPad X1','Laptop','Available',NULL),
('Lenovo ThinkPad X1','Laptop','Available',NULL),
('iPhone 14','Phone','Assigned','2000-001'),
('iPhone 14','Phone','Assigned','2000-002'),
('iPhone 14','Phone','Assigned','2000-003'),
('iPhone 14','Phone','Assigned','2000-004'),
('iPhone 14','Phone','Available',NULL);

INSERT INTO activity_log (employee_id, activity_type, department, activity_time) VALUES
('2000-001','ONBOARD','IT','2025-01-05'),
('2000-002','ONBOARD','IT','2025-01-10'),
('2000-003','ONBOARD','IT','2025-01-12'),
('2000-004','ONBOARD','HR','2025-01-15'),
('2000-005','ONBOARD','HR','2025-01-18'),
('2000-006','ONBOARD','Finance','2025-01-20'),
('2000-007','ONBOARD','Finance','2025-01-25'),
('2000-008','ONBOARD','Operations','2025-01-28'),
('2000-009','ONBOARD','IT','2025-02-01'),
('2000-010','ONBOARD','IT','2025-02-03');
GO
