CREATE DATABASE IF NOT EXISTS vitatracker;
USE vitatracker;

-- Users table
CREATE TABLE users (
  user_id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(100) NOT NULL,
  email varchar(150) NOT NULL,
  password_hash varchar(255) NOT NULL,
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  UNIQUE KEY u_name (username),
  UNIQUE KEY u_email (email)
);

-- Vitamins inventory
CREATE TABLE vitamins (
  vitamin_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  name varchar(200) NOT NULL,
  dose varchar(100) DEFAULT NULL,
  frequency varchar(100) DEFAULT NULL,
  notes text,
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (vitamin_id),
  KEY fk_user_vitamins (user_id),
  CONSTRAINT fk_user_vitamins FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);



-- Scheduling
CREATE TABLE schedules (
  schedule_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  vitamin_id int(11) NOT NULL,
  time_of_day time NOT NULL,
  days_of_week varchar(100) DEFAULT NULL, -- stores comma sep string ex: "Mon,Wed"
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (schedule_id),
  KEY fk_sched_user (user_id),
  KEY fk_sched_vit (vitamin_id),
  CONSTRAINT fk_sched_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
  CONSTRAINT fk_sched_vit FOREIGN KEY (vitamin_id) REFERENCES vitamins (vitamin_id) ON DELETE CASCADE
);


-- Logs / History
CREATE TABLE intake_logs (
  log_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  vitamin_id int(11) NOT NULL,
  taken_at datetime DEFAULT CURRENT_TIMESTAMP,
  status varchar(20) DEFAULT 'taken', -- simplified from ENUM for flexibility
  dose varchar(100) DEFAULT NULL,
  note text,
  PRIMARY KEY (log_id),
  KEY idx_log_user (user_id),
  CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
  CONSTRAINT fk_log_vit FOREIGN KEY (vitamin_id) REFERENCES vitamins (vitamin_id) ON DELETE CASCADE
);