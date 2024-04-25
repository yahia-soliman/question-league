-- create the database
CREATE DATABASE IF NOT EXISTS `questions`;
CREATE DATABASE IF NOT EXISTS `testing`;

-- create the user
CREATE USER
    IF NOT EXISTS 'question'@'%'
    IDENTIFIED BY 'answer';


-- grant access
GRANT ALL PRIVILEGES
   ON `questions`.*
   TO 'question'@'%';

GRANT ALL PRIVILEGES
   ON `testing`.*
   TO 'question'@'%';

GRANT SELECT
   ON `performance_schema`.*
   TO 'question'@'%';
