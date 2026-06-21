drop table if exists contacts;
drop table if exists instances;

create table instances (
    slug text primary key,
    name text not null
);

create table contacts (
    id integer primary key,
    instance_slug text not null references instances(slug),
    name text not null,
    email text not null default '',
    type text not null
);

insert into instances (slug, name)
values ('acme', 'Acme Distribution');

insert into contacts (instance_slug, name, email, type)
values
    ('acme', 'Ama (Fulfilment Lead)', 'ama@acme-distribution.com', 'fulfilment'),
    ('acme', 'Kofi (Warehouse)', 'kofi@acme-distribution.com', 'fulfilment'),
    ('acme', 'Esi (New Hire)', '', 'fulfilment'),
    ('acme', 'Finance', 'finance@acme-distribution.com', 'finance');
