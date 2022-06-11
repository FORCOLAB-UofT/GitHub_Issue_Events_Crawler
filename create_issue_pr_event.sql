CREATE TABLE `issue_pr_event` (
  `event` text,
  `author` text,
  `author_name` text,
  `email` text,
  `author_type` text,
  `author_association` text,
  `commit_id` text,
  `created_at` text,
  `id` text,
  `repo` text,
  `type` text,
  `state` text,
  `assignees` text,
  `label` text,
  `body` text,
  `submitted_at` text,
  `links` text,
  `old_name` text,
  `new_name` text,
  `requester` text,
  `reviewer` text,
  `dismissed_state` text,
  `dismissal_message` text,
  `repo_source` text,
  `issue_number` int DEFAULT NULL,
  `issue_type` text,
  `issue_status` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
