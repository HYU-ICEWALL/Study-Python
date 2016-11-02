drop table if exists entries;

create table submissions (
  id integer primary key autoincrement,
  user_name string not null,
  file_name string not null,
  problem_id integer not null,
  size integer default 0,
  process integer default 0,
  score integer default 0,
  stamp string not null,
  open integer default 0,
  result string,
  version string default 'PY3'
);