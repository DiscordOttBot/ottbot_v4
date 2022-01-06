CREATE TABLE IF NOT EXISTS users (
    id bigint PRIMARY KEY NOT NULL  
);

-- DROP TABLE IF EXISTS guild_config;

CREATE TABLE IF NOT EXISTS guild_config (
    "id" bigserial NOT NULL PRIMARY KEY,
    "guild_id" bigint NOT NULL UNIQUE,
    prefix varchar(5) NOT NULL DEFAULT '!'
);
