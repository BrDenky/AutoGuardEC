CREATE DATABASE CarInsuranceDB; 
USE CarInsuranceDB; 
CREATE TABLE Customer ( 
customer_id INT AUTO_INCREMENT PRIMARY KEY, 
first_name VARCHAR(50) NOT NULL, 
last_name VARCHAR(50) NOT NULL, 
address VARCHAR(100), 
phone VARCHAR(20), 
email VARCHAR(50) UNIQUE 
); 
CREATE TABLE Vehicle ( 
vehicle_id INT AUTO_INCREMENT PRIMARY KEY, 
customer_id INT, 
brand VARCHAR(50), 
model VARCHAR(50), 
year INT, 
license_plate VARCHAR(20) UNIQUE, 
FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) 
); 
CREATE TABLE Agent ( 
agent_id INT AUTO_INCREMENT PRIMARY KEY, 
name VARCHAR(100) NOT NULL, 
phone VARCHAR(20), 
email VARCHAR(50) UNIQUE 
); 
CREATE TABLE Policy ( 
    policy_id INT AUTO_INCREMENT PRIMARY KEY, 
    customer_id INT, 
    vehicle_id INT, 
    agent_id INT, 
    start_date DATE NOT NULL, 
    end_date DATE NOT NULL, 
    status ENUM('active','expired','canceled','arrears'), 
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id), 
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id), 
    FOREIGN KEY (agent_id) REFERENCES Agent(agent_id) 
); 
 
 
 
 
CREATE TABLE Coverage ( 
    coverage_id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100) NOT NULL, 
    description TEXT 
); 
 
CREATE TABLE PolicyCoverage ( 
    policy_id INT, 
    coverage_id INT, 
    PRIMARY KEY (policy_id, coverage_id), 
    FOREIGN KEY (policy_id) REFERENCES Policy(policy_id), 
    FOREIGN KEY (coverage_id) REFERENCES Coverage(coverage_id) 
); 
 
CREATE TABLE PremiumPayment ( 
    payment_id INT AUTO_INCREMENT PRIMARY KEY, 
    policy_id INT, 
    payment_date DATE NOT NULL, 
    amount DECIMAL(10,2) NOT NULL, 
    FOREIGN KEY (policy_id) REFERENCES Policy(policy_id) 
); 
 
CREATE TABLE Claim ( 
    claim_id INT AUTO_INCREMENT PRIMARY KEY, 
    policy_id INT, 
    claim_date DATE NOT NULL, 
    description TEXT, 
    status ENUM('open','closed','in review'), 
    FOREIGN KEY (policy_id) REFERENCES Policy(policy_id) 
);  
 
CREATE TABLE ClaimPayment ( 
claim_payment_id INT AUTO_INCREMENT PRIMARY KEY, 
claim_id INT, 
payment_date DATE NOT NULL, 
amount DECIMAL(10,2) NOT NULL, 
FOREIGN KEY (claim_id) REFERENCES Claim(claim_id) 
);