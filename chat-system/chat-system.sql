CREATE SCHEMA `users`;

CREATE SCHEMA `channels`;

CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `avatar_url` text,
  `created_at` datetime,
  `status` ENUM ('Online', 'Offline', 'Idle', 'Do not disturb')
);

CREATE TABLE `servers` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `icon_url` text,
  `owner_id` int NOT NULL,
  `created_at` datetime
);

CREATE TABLE `server_members` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `server_id` int NOT NULL,
  `joined_at` datetime,
  `nickname` varchar(50)
);

CREATE TABLE `roles` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `server_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `color` varchar(7),
  `permissions` text,
  `position` int
);

CREATE TABLE `member_roles` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `role_id` int NOT NULL
);

CREATE TABLE `channels` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `server_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` ENUM ('Text', 'Voice', 'Announcement') NOT NULL,
  `position` int,
  `created_at` datetime
);

CREATE TABLE `messages` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `channel_id` int NOT NULL,
  `author_id` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime
);

CREATE TABLE `direct_messages` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime
);

CREATE TABLE `reactions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `message_id` int NOT NULL,
  `user_id` int NOT NULL,
  `emoji` varchar(50) NOT NULL,
  `created_at` datetime
);

CREATE TABLE `invites` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `server_id` int NOT NULL,
  `channel_id` int,
  `inviter_id` int,
  `expires_at` datetime,
  `max_uses` int,
  `uses` int
);

CREATE UNIQUE INDEX `username` ON `users` (`username`);

CREATE UNIQUE INDEX `email` ON `users` (`email`);

CREATE INDEX `created_at` ON `users` (`created_at`);

CREATE INDEX `status` ON `users` (`status`);

CREATE INDEX `name` ON `servers` (`name`);

CREATE INDEX `created_at` ON `servers` (`created_at`);

CREATE INDEX `joined_at` ON `server_members` (`joined_at`);

CREATE INDEX `nickname` ON `server_members` (`nickname`);

CREATE INDEX `name` ON `roles` (`name`);

CREATE INDEX `position` ON `roles` (`position`);

CREATE INDEX `name` ON `channels` (`name`);

CREATE INDEX `type` ON `channels` (`type`);

CREATE INDEX `position` ON `channels` (`position`);

CREATE INDEX `created_at` ON `channels` (`created_at`);

CREATE INDEX `content` ON `messages` (`content`);

CREATE INDEX `created_at` ON `messages` (`created_at`);

CREATE INDEX `content` ON `direct_messages` (`content`);

CREATE INDEX `created_at` ON `direct_messages` (`created_at`);

CREATE INDEX `emoji` ON `reactions` (`emoji`);

CREATE INDEX `created_at` ON `reactions` (`created_at`);

CREATE INDEX `expires_at` ON `invites` (`expires_at`);

CREATE INDEX `max_uses` ON `invites` (`max_uses`);

CREATE INDEX `uses` ON `invites` (`uses`);

ALTER TABLE `servers` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `server_members` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `server_members` ADD FOREIGN KEY (`server_id`) REFERENCES `servers` (`id`);

ALTER TABLE `roles` ADD FOREIGN KEY (`server_id`) REFERENCES `servers` (`id`);

ALTER TABLE `member_roles` ADD FOREIGN KEY (`member_id`) REFERENCES `server_members` (`id`);

ALTER TABLE `member_roles` ADD FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

ALTER TABLE `channels` ADD FOREIGN KEY (`server_id`) REFERENCES `servers` (`id`);

ALTER TABLE `messages` ADD FOREIGN KEY (`channel_id`) REFERENCES `channels` (`id`);

ALTER TABLE `messages` ADD FOREIGN KEY (`author_id`) REFERENCES `users` (`id`);

ALTER TABLE `direct_messages` ADD FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`);

ALTER TABLE `direct_messages` ADD FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`);

ALTER TABLE `reactions` ADD FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`);

ALTER TABLE `reactions` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `invites` ADD FOREIGN KEY (`server_id`) REFERENCES `servers` (`id`);

ALTER TABLE `invites` ADD FOREIGN KEY (`channel_id`) REFERENCES `channels` (`id`);

ALTER TABLE `invites` ADD FOREIGN KEY (`inviter_id`) REFERENCES `users` (`id`);
