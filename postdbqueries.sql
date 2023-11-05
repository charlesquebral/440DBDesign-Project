USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `posts` (
	`postid` INT AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
    `title` varchar(50) NOT NULL,
    `description` varchar(50) NOT NULL,
  	`category` varchar(255) NOT NULL,
  	`price` varchar(100) NOT NULL,
    `date` varchar(50) NOT NULL,
    PRIMARY KEY (`postid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO posts (username, title, description, category, price, date)
VALUES ('testuser', 'testtitle', 'thisisatest', 'test, post', 10000.00, '2023-11-04');

SELECT * from posts WHERE price <= 891