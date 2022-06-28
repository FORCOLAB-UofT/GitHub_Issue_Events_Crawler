CREATE TABLE `cross_ref_PR_issue` (
  `cross_index` int NOT NULL AUTO_INCREMENT,
  `repo_source_id` int NOT NULL,
  `pr_source_id` int NOT NULL,
  `repo_target_id` int NOT NULL,
  `pr_target_id` int NOT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  `event_idx` int NOT NULL,
  PRIMARY KEY (`cross_index`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
