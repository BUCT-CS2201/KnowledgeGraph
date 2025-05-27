create table museum
(
    museum_id   bigint unsigned auto_increment comment '博物馆Id'
        primary key,
    museum_name varchar(100)                       not null comment '博物馆名字',
    description text                               null comment '博物馆介绍',
    address     varchar(100)                       null comment '博物馆线下地址',
    website_url varchar(255)                       null comment '博物馆网站链接',
    booking_url varchar(255)                       null comment '博物馆预约链接',
    create_time datetime default (now())           null comment '创建时间',
    update_time datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '修改时间'
)
    comment '博物馆表' charset = utf8mb4;


