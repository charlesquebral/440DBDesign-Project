USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `reviews` (
	`reviewid` INT AUTO_INCREMENT,
	`postid` INT,
  	`username` varchar(50) NOT NULL,
    `feedback` varchar(50) NOT NULL,
    `review` varchar(255) NOT NULL,
    `date` varchar(50) NOT NULL,
    PRIMARY KEY (`reviewid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO reviews (postid, username, feedback, review, date)
VALUES (2, 'tacotuesday', 'Excellent', 'test2', '2023-11-04');

SELECT * from reviews