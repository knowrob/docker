drop table if exists docu;
create table docu (
    id serial primary key,
    key text not null,
    text text not null
);
