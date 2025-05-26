-- DATABASE AND USERS SETUP
DROP DATABASE IF EXISTS LXC;
CREATE DATABASE LXC;

-- Admin User
CREATE OR REPLACE USER 'admin_user'@'localhost' IDENTIFIED BY 'adminpass';
GRANT ALL PRIVILEGES ON LXC.* TO 'admin_user'@'localhost';

-- Regular User
CREATE OR REPLACE USER 'regular_user'@'localhost' IDENTIFIED BY 'userpass';
GRANT ALL PRIVILEGES ON LXC.* TO 'regular_user'@'localhost';

-- SWITCH TO DATABASE
USE LXC;

-- organization_management.sql

-- Drop tables if they already exist (for clean re-run)
DROP TABLE IF EXISTS SETTLES, REQUIRES, PAYMENT, HAS_DUES, DUES, 
    EXPELLED_MEMBER, SUSPENDED_MEMBER, ALUMNI_MEMBER, INACTIVE_MEMBER, ACTIVE_MEMBER, 
    MEM_IN_ORG, MEM_HAS_MEMBERSHIP, MEMBERSHIP, ORGANIZATION, MEMBER;

-- MEMBER table
CREATE TABLE MEMBER (
    student_number VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_initial CHAR(1),
    last_name VARCHAR(50) NOT NULL,
    nickname VARCHAR(30) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    degree_program VARCHAR(50) NOT NULL
);

-- ORGANIZATION table
CREATE TABLE ORGANIZATION (
    organization_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- MEMBERSHIP table
CREATE TABLE MEMBERSHIP (
    membership_id VARCHAR(10) PRIMARY KEY,
    year_of_membership INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    semester VARCHAR(20) NOT NULL
);

-- MEM_HAS_MEMBERSHIP table
CREATE TABLE MEM_HAS_MEMBERSHIP (
    student_number VARCHAR(10),
    membership_id VARCHAR(10),
    PRIMARY KEY (student_number, membership_id),
    CONSTRAINT hasm_std_no_fk FOREIGN KEY (student_number) REFERENCES MEMBER(student_number),
    CONSTRAINT hasm_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id)
);

-- MEM_IN_ORG table
CREATE TABLE MEM_IN_ORG (
    membership_id VARCHAR(10),
    organization_id VARCHAR(10),
    PRIMARY KEY (membership_id, organization_id),
    CONSTRAINT in_ref_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id),
    CONSTRAINT in_mem_no_fk FOREIGN KEY (organization_id) REFERENCES ORGANIZATION(organization_id)
);

-- ACTIVE_MEMBER table
CREATE TABLE ACTIVE_MEMBER (
    membership_id VARCHAR(10) PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    committee VARCHAR(50) NOT NULL,
    date_of_being_active DATE NOT NULL,
    CONSTRAINT act_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id)
);

-- INACTIVE_MEMBER table
CREATE TABLE INACTIVE_MEMBER (
    membership_id VARCHAR(10) PRIMARY KEY,
    date_of_inactivity DATE NOT NULL,
    CONSTRAINT ina_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id)
);

-- ALUMNI_MEMBER table
CREATE TABLE ALUMNI_MEMBER (
    membership_id VARCHAR(10) PRIMARY KEY,
    date_of_graduation DATE NOT NULL,
    CONSTRAINT alum_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id)
);

-- SUSPENDED_MEMBER table
CREATE TABLE SUSPENDED_MEMBER (
    membership_id VARCHAR(10) PRIMARY KEY,
    date_of_suspension DATE NOT NULL,
    CONSTRAINT susp_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id)
);

-- EXPELLED_MEMBER table
CREATE TABLE EXPELLED_MEMBER (
    membership_id VARCHAR(10) PRIMARY KEY,
    date_of_expulsion DATE NOT NULL,
    CONSTRAINT expe_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id)
);

-- DUES table
CREATE TABLE DUES (
    due_id VARCHAR(10) PRIMARY KEY,
    amount_due DECIMAL(10, 2) NOT NULL,
    due_date DATE NOT NULL,
    due_status VARCHAR(20) NOT NULL
);

-- HAS_DUES table
CREATE TABLE HAS_DUES (
    membership_id VARCHAR(15),
    due_id VARCHAR(15),
    PRIMARY KEY (membership_id, due_id),
    CONSTRAINT hasd_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id),
    CONSTRAINT hasd_due_no_fk FOREIGN KEY (due_id) REFERENCES DUES(due_id)
);

-- PAYMENT table
CREATE TABLE PAYMENT (
    reference_id VARCHAR(20) PRIMARY KEY
);

-- SETTLES table
CREATE TABLE SETTLES (
    reference_id VARCHAR(20),
    due_id VARCHAR(15),
    payment_date DATE NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (reference_id, due_id),
    CONSTRAINT set_ref_no_fk FOREIGN KEY (reference_id) REFERENCES PAYMENT(reference_id),
    CONSTRAINT set_due_no_fk FOREIGN KEY (due_id) REFERENCES DUES(due_id)
);

-- REQUIRES table
CREATE TABLE REQUIRES (
    membership_id VARCHAR(15),
    reference_id VARCHAR(20),
    PRIMARY KEY (membership_id, reference_id),
    CONSTRAINT req_mem_no_fk FOREIGN KEY (membership_id) REFERENCES MEMBERSHIP(membership_id),
    CONSTRAINT req_ref_no_fk FOREIGN KEY (reference_id) REFERENCES PAYMENT(reference_id)
);

-- Core Functionalities

-- Insert sample organization
INSERT INTO ORGANIZATION (organization_id, name) VALUES ("ORG001", "UPLB Database Society");
INSERT INTO ORGANIZATION (organization_id, name) VALUES ("ORG002", "UPLB Math Circle");
INSERT INTO ORGANIZATION (organization_id, name) VALUES ("ORG003", "UPLB Programming Guild");

-- Add a member and their related entries
-- database society
INSERT INTO MEMBER VALUES ("2023-00001", "Reina", "D", "Cruz", "Rei", "Female", "BS CS");
INSERT INTO MEMBERSHIP VALUES ("C004", 2023, "2023-2024", "1st Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00001", "C004");
INSERT INTO MEM_IN_ORG VALUES ("C004", "ORG001");
INSERT INTO ACTIVE_MEMBER VALUES ("C004", "Vice President", "Database", "2023-08-01");

INSERT INTO MEMBER VALUES ("2023-00002", "Liam", "E", "Santos", "Liam", "Male", "BS IS");
INSERT INTO MEMBERSHIP VALUES ("C005", 2023, "2023-2024", "2nd Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00002", "C005");
INSERT INTO MEM_IN_ORG VALUES ("C005", "ORG001");
INSERT INTO ACTIVE_MEMBER VALUES ("C005", "Member", "Database", "2024-01-15");

INSERT INTO MEMBER VALUES ("2023-00003", "Celine", "F", "Reyes", "Cels", "Female", "BS STAT");
INSERT INTO MEMBERSHIP VALUES ("C006", 2024, "2024-2025", "1st Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00003", "C006");
INSERT INTO MEM_IN_ORG VALUES ("C006", "ORG001");
INSERT INTO ACTIVE_MEMBER VALUES ("C006", "Member", "Database", "2024-08-10");


-- math circle
INSERT INTO MEMBER VALUES ("2023-00004", "Marcus", "G", "Lopez", "Marc", "Male", "BS MATH");
INSERT INTO MEMBERSHIP VALUES ("C007", 2023, "2023-2024", "2nd Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00004", "C007");
INSERT INTO MEM_IN_ORG VALUES ("C007", "ORG002");
INSERT INTO ACTIVE_MEMBER VALUES ("C007", "Secretary", "Academic", "2023-11-10");

INSERT INTO MEMBER VALUES ("2023-00005", "Inah", "H", "Garcia", "Inah", "Female", "BS APMATH");
INSERT INTO MEMBERSHIP VALUES ("C008", 2023, "2023-2024", "1st Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00005", "C008");
INSERT INTO MEM_IN_ORG VALUES ("C008", "ORG002");
INSERT INTO ACTIVE_MEMBER VALUES ("C008", "Member", "Publications", "2023-08-12");

INSERT INTO MEMBER VALUES ("2023-00006", "Jordan", "I", "Tan", "Jordy", "Male", "BS CS");
INSERT INTO MEMBERSHIP VALUES ("C009", 2024, "2024-2025", "1st Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00006", "C009");
INSERT INTO MEM_IN_ORG VALUES ("C009", "ORG002");
INSERT INTO ACTIVE_MEMBER VALUES ("C009", "Member", "Academic", "2024-08-20");


--programming guild
INSERT INTO MEMBER VALUES ("2023-00007", "Ella", "J", "Villanueva", "Ella", "Female", "BS CS");
INSERT INTO MEMBERSHIP VALUES ("C010", 2023, "2023-2024", "1st Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00007", "C010");
INSERT INTO MEM_IN_ORG VALUES ("C010", "ORG003");
INSERT INTO ACTIVE_MEMBER VALUES ("C010", "Project Head", "Dev", "2023-08-25");

INSERT INTO MEMBER VALUES ("2023-00008", "Kyle", "K", "Domingo", "Ky", "Male", "BS ECE");
INSERT INTO MEMBERSHIP VALUES ("C011", 2023, "2023-2024", "2nd Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00008", "C011");
INSERT INTO MEM_IN_ORG VALUES ("C011", "ORG003");
INSERT INTO ACTIVE_MEMBER VALUES ("C011", "Member", "Tech", "2024-01-10");

INSERT INTO MEMBER VALUES ("2023-00009", "Samantha", "L", "Chan", "Sam", "Female", "BS CS");
INSERT INTO MEMBERSHIP VALUES ("C012", 2024, "2024-2025", "1st Semester");
INSERT INTO MEM_HAS_MEMBERSHIP VALUES ("2023-00009", "C012");
INSERT INTO MEM_IN_ORG VALUES ("C012", "ORG003");
INSERT INTO ACTIVE_MEMBER VALUES ("C012", "Member", "Dev", "2024-08-30");

-- MEMBERS
INSERT INTO MEMBER VALUES 
('2023000010', 'Maria', 'D', 'Reyes', 'Yaya', 'Female', 'BS CS'),
('2023000020', 'Juan', 'S', 'Dela Cruz', 'Juancho', 'Male', 'BS MATH'),
('2023000030', 'Ana', 'L', 'Santos', 'Nana', 'Female', 'BS AMAT'),
('2023000040', 'Carlos', 'M', 'Lopez', 'Caloy', 'Male', 'BS CS'),
('2023000050', 'Luna', 'R', 'Garcia', 'Lulu', 'Female', 'BS MATH'),
('2023000060', 'Miguel', 'T', 'Fernandez', 'Migz', 'Male', 'BS AMAT'),
('2023000070', 'Bianca', 'E', 'Tan', 'Bianx', 'Female', 'BS CS'),
('2023000080', 'Marco', 'C', 'Rivera', 'Marky', 'Male', 'BS MATH'),
('2023000090', 'Elena', 'A', 'Torres', 'Len', 'Female', 'BS AMAT');

-- MEMBERSHIPS
INSERT INTO MEMBERSHIP VALUES 
('M001', 2023, '2023-2024', '1st'),
('M002', 2022, '2022-2023', '2nd'),
('M003', 2024, '2024-2025', '1st'),
('M004', 2021, '2021-2022', '1st'),
('M005', 2020, '2020-2021', '2nd'),
('M006', 2023, '2023-2024', '2nd'),
('M007', 2021, '2021-2022', '2nd'),
('M008', 2022, '2022-2023', '1st'),
('M009', 2024, '2024-2025', '1st');

-- LINK MEMBERS TO MEMBERSHIPS
INSERT INTO MEM_HAS_MEMBERSHIP VALUES 
('2023000010', 'M001'),
('2023000020', 'M002'),
('2023000030', 'M003'),
('2023000040', 'M004'),
('2023000050', 'M005'),
('2023000060', 'M006'),
('2023000070', 'M007'),
('2023000080', 'M008'),
('2023000090', 'M009');

-- LINK MEMBERSHIPS TO ORGS
INSERT INTO MEM_IN_ORG VALUES 
('M001', 'ORG001'), -- Inactive
('M002', 'ORG002'), -- Inactive
('M003', 'ORG003'), -- Inactive
('M004', 'ORG001'), -- Alumni
('M005', 'ORG002'), -- Alumni
('M006', 'ORG003'), -- Alumni
('M007', 'ORG001'), -- Suspended
('M008', 'ORG002'), -- Suspended
('M009', 'ORG003'); -- Expelled

-- INACTIVE MEMBERS
INSERT INTO INACTIVE_MEMBER VALUES 
('M001', '2024-04-01'),
('M002', '2023-11-10'),
('M003', '2025-01-15');

-- ALUMNI MEMBERS
INSERT INTO ALUMNI_MEMBER VALUES 
('M004', '2022-06-30'),
('M005', '2021-06-30'),
('M006', '2024-06-30');

-- SUSPENDED MEMBERS
INSERT INTO SUSPENDED_MEMBER VALUES 
('M007', '2022-03-15'),
('M008', '2023-09-01');

-- EXPELLED MEMBER
INSERT INTO EXPELLED_MEMBER VALUES 
('M009', '2025-05-01');


-- DUES
INSERT INTO DUES VALUES ("D001", 300.00, '2024-09-01', "Unpaid");
INSERT INTO DUES VALUES ("D002", 250.00, '2024-09-15', "Unpaid");
INSERT INTO DUES VALUES ("D003", 200.00, '2024-10-01', "Unpaid");

-- HAS_DUES: linking dues to members
INSERT INTO HAS_DUES VALUES ("C004", "D001");  -- Reina
INSERT INTO HAS_DUES VALUES ("C007", "D002");  -- Marcus
INSERT INTO HAS_DUES VALUES ("C010", "D003");  -- Ella


-- PAYMENT
INSERT INTO PAYMENT VALUES ("P001");
INSERT INTO PAYMENT VALUES ("P002");
INSERT INTO PAYMENT VALUES ("P003");

-- SETTLES: log actual payments
INSERT INTO SETTLES VALUES ("P001", "D001", '2024-09-02', 300.00);  -- Reina paid
INSERT INTO SETTLES VALUES ("P002", "D002", '2024-09-16', 250.00);  -- Marcus paid
INSERT INTO SETTLES VALUES ("P003", "D003", '2024-10-01', 200.00);  -- Ella paid

-- REQUIRES: associate payments with membership
INSERT INTO REQUIRES VALUES ("C004", "P001");  -- Reina
INSERT INTO REQUIRES VALUES ("C007", "P002");  -- Marcus
INSERT INTO REQUIRES VALUES ("C010", "P003");  -- Ella

--set dues status to 'Paid' for the dues that have been settled
UPDATE DUES SET due_status = 'Paid' WHERE due_ID = 'D001';
UPDATE DUES SET due_status = 'Paid' WHERE due_ID = 'D002';
UPDATE DUES SET due_status = 'Paid' WHERE due_ID = 'D003';


-- NOW REVOKE regular_user’s access to everything EXCEPT SELECT
REVOKE ALL PRIVILEGES ON LXC.* FROM 'regular_user'@'localhost';
GRANT SELECT ON LXC.* TO 'regular_user'@'localhost';