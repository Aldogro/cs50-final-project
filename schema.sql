DROP TABLE IF EXISTS people;

CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    document_number NUMERIC NOT NULL,
    phone NUMERIC NOT NULL,
    user_address TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
