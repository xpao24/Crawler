-- auto-generated definition
create table jobs_crawler.task
(
  id         bigint auto_increment
    primary key,
  priority   int          null,
  type       int          null,
  state      int          null,
  link       varchar(200) null,
  start_time bigint       null,
  end_time   bigint       null,
  title      varchar(200) null,
  tag        varchar(200) null,
  ctime      bigint       null,
  utime      bigint       null
);


