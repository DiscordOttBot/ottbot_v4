-- DROP TABLE IF EXISTS users;

-- Used by dashboard
CREATE TABLE IF NOT EXISTS users (
    id bigserial NOT NULL PRIMARY KEY,
    discord_id varchar(32) UNIQUE NOT NULL,
    access_token varchar(255) NOT NULL,
    refresh_token varchar(255) NOT NULL,
    username varchar(32) NOT NULL,
    discriminator varchar(4) NOT NULL
);

-- DROP TABLE IF EXISTS guild_config;

CREATE TABLE IF NOT EXISTS guild_config (
    id bigserial NOT NULL PRIMARY KEY,
    guild_id bigint NOT NULL UNIQUE,
    prefix varchar(5) NOT NULL DEFAULT '!',
    welcome_channel_id bigint
);

DROP TABLE IF EXISTS currency;

CREATE TABLE IF NOT EXISTS currency (
    id bigserial NOT NULL PRIMARY KEY,
    user_id bigint NOT NULL,
    balance bigint NOT NULL DEFAULT 0,
    bank bigint NOT NULL DEFAULT 0,
    last_daily TIMESTAMP
);