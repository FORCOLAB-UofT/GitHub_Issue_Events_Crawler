CREATE TABLE `scraped_repos` (
  `scraped_index` int NOT NULL AUTO_INCREMENT,
  `repo_index` int NOT NULL,
  `pr_issues_count` int NOT NULL,
  `repo_name` varchar(500) DEFAULT NULL,
  `scraped_at` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`scraped_index`),
  UNIQUE KEY `repo_name_UNIQUE` (`repo_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
