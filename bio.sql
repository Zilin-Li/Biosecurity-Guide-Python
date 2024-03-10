CREATE TABLE role (
	id INT AUTO_INCREMENT PRIMARY KEY,
	role_name VARCHAR(50) NOT NULL
);

CREATE TABLE position (
    id INT AUTO_INCREMENT PRIMARY KEY,
    position_name VARCHAR(50) NOT NULL
);

CREATE TABLE department (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(128) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    first_name VARCHAR(50), 
    last_name VARCHAR(50), 
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),  
    join_date DATETIME,
	role_id INT,
    status TINYINT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id VARCHAR(25),
    hire_date DATETIME,  
    user_id INT,
    position_id INT,
    department_id INT,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (position_id) REFERENCES position (id),
    FOREIGN KEY (department_id) REFERENCES department (id)
);

CREATE TABLE horticulturalist(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    horticulturalist_id VARCHAR(25), 
    address VARCHAR(255), 
    FOREIGN KEY (user_id) REFERENCES user(id)
);



CREATE TABLE biosecurity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    common_name VARCHAR(100),
    scientific_name VARCHAR(100),
    key_char text NULL,
    biology text NULL,
    impact  text NULL,
    source_url VARCHAR(255),
    is_present_in_nz TINYINT NOT NULL    
);

CREATE TABLE biosecurityimage (
	id INT AUTO_INCREMENT PRIMARY KEY,
	biosecurity_id int,
	image_path VARCHAR(255),
	description text NULL,
	is_primary tinyint,
    FOREIGN KEY (biosecurity_id) REFERENCES biosecurity (id)
);

