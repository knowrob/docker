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
INSERT INTO Platform VALUES(3, 'Perception');


drop table if exists tag;
create table tag (
    id serial primary key,
    name text not null
);
