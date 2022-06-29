CREATE TABLE `repo_list` (
  `repo_index` int NOT NULL AUTO_INCREMENT,
  `repo_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`repo_index`),
  UNIQUE KEY `repo_name_UNIQUE` (`repo_name`)
) ENGINE=InnoDB AUTO_INCREMENT=655 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

