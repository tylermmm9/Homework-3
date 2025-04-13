CREATE TABLE IF NOT EXISTS `skills` (
`skill_id`              int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'The position id',
`experience_id`         int(11)       NOT NULL 				    COMMENT 'FK:The instiution id',
`name`                  varchar(100)  NOT NULL					COMMENT 'My title in this position',
`skill_level`           varchar(500)  NOT NULL                  COMMENT 'My responsibilities in this position',
PRIMARY KEY (`skill_id`),
FOREIGN KEY (`experience_id`) REFERENCES experiences(`experience_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Positions I have held";
