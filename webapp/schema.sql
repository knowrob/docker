drop table if exists tutorial;
create table tutorial (
	id integer primary key autoincrement,
	cat_id text not null,
	cat_title text not null,
	title text not null,
	text text not null
);

drop table if exists users;
create table users (
        id integer primary key autoincrement,
        username text unique not null,
        email text not null,
        passwd text not null,
        container_id text not null
);

