drop table if exists project;
create table project (
    id serial primary key,
    name text not null,
    url text not null
);
INSERT INTO Project VALUES(0, 'ACAT', 'http://www.acat-project.eu/');
INSERT INTO Project VALUES(1, 'RoboHow', 'https://robohow.eu/');
INSERT INTO Project VALUES(2, 'SAPHARI', 'http://www.saphari.eu/');
INSERT INTO Project VALUES(3, 'RoboEarth', 'http://www.roboearth.org');
INSERT INTO Project VALUES(4, 'SHERPA', 'http://www.sherpa-project.eu/sherpa/');


drop table if exists platform;
create table platform (
    id serial primary key,
    name text not null
);
INSERT INTO Platform VALUES(0, 'Robotic Agents');
INSERT INTO Platform VALUES(1, 'Simulation');
INSERT INTO Platform VALUES(2, 'Motion Capturing');
INSERT INTO Platform VALUES(3, 'RoboSherlock');
INSERT INTO Platform VALUES(4, 'CRAM');
INSERT INTO Platform VALUES(5, 'KnowRob');
INSERT INTO Platform VALUES(6, 'PRAC');


drop table if exists role;
create table role (
    id serial primary key,
    name text not null
);
INSERT INTO Role VALUES(0, 'admin');
INSERT INTO Role VALUES(1, 'reviewer');
INSERT INTO Role VALUES(2, 'user');
INSERT INTO Role VALUES(3, 'editor');


drop table if exists tag;
create table tag (
    id serial primary key,
    name text not null
);
