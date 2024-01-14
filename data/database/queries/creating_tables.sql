create table if not exists User(
	id varchar(256),
	bungie_name	varchar(256) unique not null, 
    
    primary key(id)
    );

create table if not exists Raid(
	id			int			 auto_increment,
	raid		varchar(256) not null,
    token_id    varchar(256) not null,
    player1 	varchar(256),
    player2 	varchar(256),
    player3 	varchar(256),
    player4 	varchar(256),
    player5 	varchar(256),
    player6 	varchar(256),
    
    primary key (id),
    foreign key (player1) references user(id),
    foreign key (player2) references user(id),
    foreign key (player3) references user(id),
    foreign key (player4) references user(id),
    foreign key (player5) references user(id),
    foreign key (player6) references user(id)
    );
    
create table if not exists Dungeon(
	id			int			 auto_increment,
	dungeon		varchar(256) not null,
    token_id    varchar(256) not null,
    player1 	varchar(256),
    player2 	varchar(256),
    player3 	varchar(256),
    
    primary key (id),
    foreign key (player1) references user(id),
    foreign key (player2) references user(id),
    foreign key (player3) references user(id)
    );