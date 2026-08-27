
-- create the consultants table
CREATE TABLE consultants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,

    CONSTRAINT consultant_name_not_empty
        CHECK (LENGTH(TRIM(name)) > 0),

    CONSTRAINT consultant_email_not_empty
        CHECK (LENGTH(TRIM(email)) > 0)
);

-- create the customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,

    CONSTRAINT customer_name_not_empty
        CHECK (LENGTH(TRIM(name)) > 0)
);

-- create the extension used in the time_entries table
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- create the time_entries table
CREATE TABLE time_entries (
    id SERIAL PRIMARY KEY,

    consultant_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,

    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,

    lunch_break INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT fk_consultant
        FOREIGN KEY (consultant_id)
        REFERENCES consultants(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT,

    CONSTRAINT valid_time
        CHECK (end_time > start_time),

    CONSTRAINT valid_lunch_break
        CHECK (lunch_break >= 0),

    CONSTRAINT lunch_not_longer_than_workday
        CHECK (
            lunch_break <=
            EXTRACT(EPOCH FROM (end_time - start_time)) / 60
        ),

    CONSTRAINT no_overlapping_consultant_entries
        EXCLUDE USING GIST (
            consultant_id WITH =,
            tsrange(start_time, end_time, '[)') WITH &&
        )
);