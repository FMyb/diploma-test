create table if not exists checkpoints
(
    checkpoint_id varchar(50) not null primary key,
    name          varchar(50)
);

create table if not exists vms
(
    vm_id varchar(50) not null primary key,
    name  varchar(50) not null,
    host  varchar(50) not null,
    token varchar(50) not null,
    busy  varchar(50)
);
