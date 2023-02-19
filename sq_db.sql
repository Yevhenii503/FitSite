CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY,
title text NOT NULL,
text text NOT NULL,
url text NOT NULL,
time integer NOT NULL
);