CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `accounts` (
  	`username` varchar(50) NOT NULL,
    `firstname` varchar(50) NOT NULL,
    `lastname` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `accounts` (`username`, `firstname`, `lastname`, `password`, `email`) VALUES ('testuser', 'testname', 'testlastname','0ef15de6149819f2d10fc25b8c994b574245f193', 'test@test.com');

SELECT * FROM accounts
