drop table if exists posts;

create table posts(
    id integer primary key autoincrement,
    author text not null,
    created timestamp not null default current_timestamp,
    text text not null,
    image text not null,
    likes integer not null,
    dislikes integer not null
);