CREATE TABLE `pr_issue` (
  `issue_index` int NOT NULL AUTO_INCREMENT,
  `repo_index` int NOT NULL,
  `issue_id` int NOT NULL,
  `issue_or_pr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `closed_at` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `author_login` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ,
  `issue_status` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ,
  PRIMARY KEY (`issue_index`),
  UNIQUE KEY `issue_index_UNIQUE` (`issue_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
