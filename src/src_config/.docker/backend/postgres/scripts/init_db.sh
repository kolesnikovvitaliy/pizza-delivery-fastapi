#!/bin/bash
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$POSTGRES_DB"  <<-EOSQL
    DROP DATABASE IF EXISTS postgres WITH (FORCE);
    create schema if not exists "test";
    create table test.todo (
       id serial primary key,
       done boolean not null default false,
       task text not null,
       due timestamptz
    );

EOSQL