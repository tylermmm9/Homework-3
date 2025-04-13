CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The comment id',
`name`              varchar(100)  NOT NULL                  COMMENT 'The commentators name',
`email`             varchar(100)  NOT NULL                  COMMENT 'The commentators email',
`comment`           varchar(500)  NOT NULL                  COMMENT 'The commentators comment',
PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="user feedback about website";