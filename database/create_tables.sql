USE financedb;
CREATE TABLE IF NOT EXISTS Users (user_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(250) NOT NULL,email VARCHAR(250) UNIQUE KEY NOT NULL,password_hash VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,last_login TIMESTAMP NULL);
