-- ===============================================================================
-- Database Initialization Script - AutoGuardEC
-- ===============================================================================
-- This script runs automatically when the MySQL container is first created

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS CarInsuranceDB
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Use the database
USE CarInsuranceDB;

-- Grant privileges (optional - for additional security you can create a separate user)
-- CREATE USER IF NOT EXISTS 'autoguardec'@'%' IDENTIFIED BY 'secure_password';
-- GRANT ALL PRIVILEGES ON CarInsuranceDB.* TO 'autoguardec'@'%';
-- FLUSH PRIVILEGES;

-- Note: Tables will be created automatically by SQLAlchemy's db.create_all()
-- when the Flask application starts
