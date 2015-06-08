drop table if exists tutorial;
create table tutorial (
    id serial primary key,
    cat_id text not null,
    cat_title text not null,
    title text not null,
    text text not null,
    page integer not null
);