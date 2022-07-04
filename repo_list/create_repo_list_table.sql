CREATE TABLE `repo_list` (
  `repo_index` int NOT NULL AUTO_INCREMENT,
  `repo_name` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`repo_index`),
  UNIQUE KEY `repo_name_UNIQUE` (`repo_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
