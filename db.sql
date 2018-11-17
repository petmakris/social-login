CREATE SCHEMA socialbuttons ;

drop table socialbuttons.users;

CREATE TABLE socialbuttons.users (
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(128) NOT NULL DEFAULT '',
    last_name VARCHAR(128) NOT NULL DEFAULT '',
    email VARCHAR(128) NOT NULL DEFAULT '',
    password VARCHAR(128) NOT NULL DEFAULT '',
    devlang VARCHAR(128) NOT NULL DEFAULT '',
    google_id VARCHAR(128) NULL DEFAULT '',
    google_email VARCHAR(128) NULL DEFAULT '',
    facebook_id VARCHAR(128) NULL DEFAULT '',
    facebook_email VARCHAR(128) NULL DEFAULT '',

    PRIMARY KEY (id),
    UNIQUE INDEX user_id_UNIQUE (id ASC),
    UNIQUE INDEX email_UNIQUE (email ASC),
    UNIQUE INDEX google_id_UNIQUE (google_id ASC),
    UNIQUE INDEX google_email_UNIQUE (google_email ASC),
    UNIQUE INDEX facebook_id_UNIQUE (facebook_id ASC),
    UNIQUE INDEX facebook_email_UNIQUE (facebook_email ASC)
);

