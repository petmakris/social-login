CREATE SCHEMA socialbuttons ;

CREATE TABLE socialbuttons.users (
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(128) NULL DEFAULT NULL,
    last_name VARCHAR(128) NULL DEFAULT NULL,
    email VARCHAR(128) NULL DEFAULT NULL,
    password VARCHAR(128) NULL DEFAULT NULL,
    devlang VARCHAR(128) NULL DEFAULT NULL,

    google_id VARCHAR(128) NULL DEFAULT NULL,
    google_email VARCHAR(128) NULL DEFAULT NULL,
    facebook_id VARCHAR(128) NULL DEFAULT NULL,
    facebook_email VARCHAR(128) NULL DEFAULT NULL,

    PRIMARY KEY (user_id),
    UNIQUE INDEX user_id_UNIQUE (user_id ASC),
    UNIQUE INDEX email_UNIQUE (email ASC),
    UNIQUE INDEX google_id_UNIQUE (google_id ASC),
    UNIQUE INDEX google_email_UNIQUE (google_email ASC),
    UNIQUE INDEX facebook_id_UNIQUE (facebook_id ASC),
    UNIQUE INDEX facebook_email_UNIQUE (facebook_email ASC)
);

