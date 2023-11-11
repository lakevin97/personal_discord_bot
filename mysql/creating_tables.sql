drop table if exists flawless_table;
drop table if exists activity;
drop table if exists user;

create table if not exists user(
	id varchar(256),
	bungie_name	varchar(256) unique not null, 
    
    primary key(id)
    );

create table if not exists activity(
	id			int			auto_increment,
	activity	varchar(256) not null,
	time_date   varchar(256) not null,
    created_by 	varchar(256) not null,
    player2 	varchar(256),
    player3 	varchar(256),
    player4 	varchar(256),
    player5 	varchar(256),
    player6 	varchar(256),
    
    primary key (id),
    foreign key (created_by) references user(id),
    foreign key (player2) references user(id),
    foreign key (player3) references user(id),
    foreign key (player4) references user(id),
    foreign key (player5) references user(id),
    foreign key (player6) references user(id)
    );

create table if not exists flawless_table(
	id					int			auto_increment,
    win					bool		 null,
    player	 			varchar(256) not null,
    flawless_date 		varchar(256) null,
	flawless_weekend	varchar(256) unique not null,
    
    primary key(id),
    foreign key (player) references user(id)
    );