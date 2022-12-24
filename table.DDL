--
-- Create model Memo
--
CREATE TABLE `account_books_memo` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `spend_price` integer UNSIGNED NOT NULL,
    `content` longtext NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `deleted_at` datetime(6) NULL,
    `user_id` bigint NOT NULL);

--
-- Create model Url
--
CREATE TABLE `account_books_url` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `link` varchar(32) NOT NULL UNIQUE,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `expired_at` datetime(6) NOT NULL,
    `memo_id` bigint NOT NULL UNIQUE
);

ALTER TABLE `account_books_memo` ADD CONSTRAINT `account_books_memo_user_id_357a5066_fk_accounts_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

ALTER TABLE `account_books_url` ADD CONSTRAINT `account_books_url_memo_id_02450587_fk_account_books_memo_id`
    FOREIGN KEY (`memo_id`) REFERENCES `account_books_memo` (`id`);


--
-- Create model User
--
CREATE TABLE `accounts_user` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `password` varchar(128) NOT NULL,
    `last_login` datetime(6) NULL,
    `email` varchar(30) NOT NULL UNIQUE,
    `is_superuser` bool NOT NULL,
    `is_active` bool NOT NULL,
    `is_staff` bool NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL
);