CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `favorites` (
	`favoriteid` INT AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`favorite` varchar(100) NOT NULL,
    `type` varchar(50) NOT NULL,
    PRIMARY KEY (`favoriteid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `favorites` (`username`, `favorite`, `type`) VALUES ('adventureseeker22', 'silverstorm45', 'user');

SELECT * FROM favorites;

SELECT DISTINCT favorite
FROM favorites
WHERE 1=1
	AND type = 'users'
    AND (username = 'silverstorm45' OR username = 'code_ninja')
    AND (favorite <> 'silverstorm45' AND favorite <> 'code_ninja')
GROUP BY favorite
HAVING COUNT(*) > 1
