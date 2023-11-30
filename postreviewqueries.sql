USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `reviews` (
	`reviewid` INT AUTO_INCREMENT,
	`postid` INT,
    `poster` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
    `feedback` varchar(50) NOT NULL,
    `review` varchar(255) NOT NULL,
    `date` varchar(50) NOT NULL,
    PRIMARY KEY (`reviewid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

SELECT * from reviews;

INSERT INTO reviews (postid, poster, username, feedback, review, date)
VALUES ('3', 'username2', 'username7', 'Poor', 'cool', '2023-11-29');