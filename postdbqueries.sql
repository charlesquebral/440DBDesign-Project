USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `posts` (
	`postid` INT AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
    `title` varchar(50) NOT NULL,
    `description` varchar(50) NOT NULL,
  	`category` varchar(255) NOT NULL,
  	`price` float NOT NULL,
    `date` varchar(50) NOT NULL,
    PRIMARY KEY (`postid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO posts (username, title, description, category, price, date)
VALUES ('username3', 'testtitle', 'thisisatest', 'Category0, Category5', 10000.00, '2023-11-29');

SELECT username
FROM posts
WHERE date = '2023-11-29'
GROUP BY username
HAVING COUNT(*) = (
    SELECT MAX(post_count)
    FROM (
        SELECT COUNT(*) AS post_count
        FROM posts
        WHERE date = '2023-11-29'
        GROUP BY username
    ) AS counts
);

SELECT * FROM posts;

#WE WORKING HERE RIGHT NOW
SELECT DISTINCT t2.username
FROM posts t1
JOIN posts t2 ON t1.date = t2.date AND t1.postid <> t2.postid AND t1.username = t2.username
WHERE (t1.category LIKE '%Category0%' AND t2.category LIKE '%Category5%')
   OR (t1.category LIKE '%Category5%' AND t2.category LIKE '%Category0%')
GROUP BY t2.username, t2.date
HAVING COUNT(t2.postid) >= 2;

INSERT INTO posts (username, title, description, category, price, date)
VALUES ('username4', 'testtitle4', 'thisisatest', 'Category0, Category8', 10000.00, '2023-11-29');

SELECT DISTINCT username
FROM posts
WHERE username NOT IN (
	SELECT DISTINCT poster
	FROM reviews
    WHERE feedback = 'Excellent'
	GROUP BY poster, postid
	HAVING COUNT(*) >= 3
);

SELECT DISTINCT username
FROM reviews r1
WHERE feedback = 'Poor'
AND NOT EXISTS (
    SELECT 1
    FROM reviews r2
    WHERE r1.username = r2.username
    AND r2.feedback != 'Poor'
);

SELECT p.postid,
p.username,
r.poster,
r.username,
r.feedback
FROM posts p
JOIN reviews r ON r.postid = p.postid
GROUP BY r.postid;

SELECT DISTINCT postid
FROM reviews r1
WHERE NOT EXISTS (
    SELECT 1
    FROM reviews r2
    WHERE r1.postid = r2.postid
    AND r2.feedback IN ('Poor', 'Fair')
)
AND r1.poster = 'username0';

SELECT * FROM posts WHERE username = 'username0';