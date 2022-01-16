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
    last_daily timestamp
);

-- Trigger for deleting old invites

-- CREATE FUNCTION delete_old_invites() RETURNS trigger
--     LANGUAGE plpgsql
--     AS $$
-- BEGIN
--   DELETE FROM expire_table WHERE timestamp < NOW() - INTERVAL '1 minute';
--   RETURN NEW;
-- END;
-- $$;

CREATE TABLE IF NOT EXISTS invites (
    id bigserial NOT NULL PRIMARY KEY,
    user_id bigint NOT NULL,
    guild_id bigint NOT NULL,
    code varchar(32) NOT NULL,
    uses bigint NOT NULL DEFAULT 0,
    expires_at timestampz
);

-- CREATE TRIGGER delete_old_invites_trigger
--     AFTER INSERT ON invites
--     EXECUTE PROCEDURE delete_old_invites();

CREATE TABLE IF NOT EXISTS auto_roles (
    id bigserial NOT NULL PRIMARY KEY,
    guild_id bigint NOT NULL,
    role_id bigint NOT NULL UNIQUE
);