create table museum_image
(
    image_id  bigint unsigned auto_increment
        primary key,
    img_url   text            null comment '博物馆图片地址',
    museum_id bigint unsigned not null comment '博物馆ID',
    constraint museum_image_museum_museum_id_fk
        foreign key (museum_id) references museum (museum_id)
)
    comment '博物馆图片表' charset = utf8mb4;


