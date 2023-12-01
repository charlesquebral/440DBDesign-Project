USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `reviews` (
	`reviewid` INT AUTO_INCREMENT,
	`postid` INT,
    `poster` varchar(50) NOT NULL,
  	`reviewer` varchar(50) NOT NULL,
    `feedback` varchar(50) NOT NULL,
    `review` varchar(255) NOT NULL,
    `date` varchar(50) NOT NULL,
    PRIMARY KEY (`reviewid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO reviews (postid, poster, reviewer, feedback, review, date)
VALUES ('1', 'silverstorm45', 'code_ninja', 'Excellent', 'This is excellent!', '2023-11-29');
    
SELECT
	r1.poster AS poster1,
	r1.reviewer AS reviewer1,
	(SELECT COUNT(*) FROM posts p WHERE p.username = r1.poster) AS post_count_r1
FROM reviews r1
JOIN 
	reviews r2 ON r1.poster = r2.reviewer AND r1.reviewer = r2.poster
WHERE 
	(r1.feedback = 'Excellent' AND r2.feedback = 'Excellent')
GROUP BY
    r1.poster, r1.reviewer, r2.poster, r2.reviewer, r2.feedback
HAVING COUNT(r2.poster) = post_count_r1;

SELECT DISTINCT username FROM accounts WHERE username NOT IN ( SELECT DISTINCT reviewer FROM reviews WHERE feedback = 'Poor' GROUP BY reviewer HAVING COUNT(*) >= 1);

SELECT DISTINCT reviewer FROM reviews r1 WHERE feedback = 'Poor' AND NOT EXISTS ( SELECT 1 FROM reviews r2 WHERE r1.reviewer = r2.reviewer AND r2.feedback != 'Poor');