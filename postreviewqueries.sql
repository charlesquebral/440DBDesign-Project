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
VALUES ('4', 'username3', 'username78', 'Poor', 'cool', '2023-11-29');

DELETE FROM reviews WHERE reviewid = '7' OR reviewid = '8';

SELECT username
FROM reviews
WHERE username IN (

);

SELECT R1.poster, R1.username
FROM reviews R1
LEFT JOIN reviews R2 ON R1.poster = R2.username
                   AND R1.username = R2.poster
                   AND R1.feedback = 'Excellent'
                   AND R2.feedback = 'Excellent'
WHERE R2.poster IS NULL
