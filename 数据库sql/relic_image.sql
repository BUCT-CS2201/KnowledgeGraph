create table relic_image
(
    image_id bigint unsigned auto_increment
        primary key,
    img_url  text            null comment '文物图片地址',
    relic_id bigint unsigned null comment '文物id',
    constraint relic_image_cultural_relic_relic_id_fk
        foreign key (relic_id) references cultural_relic (relic_id)
)
    comment '图片表' charset = utf8mb4;


