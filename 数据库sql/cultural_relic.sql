create table cultural_relic
(
    relic_id    bigint unsigned auto_increment comment '文物id'
        primary key,
    museum_id   bigint unsigned                           not null comment '博物馆id',
    name        varchar(50)                               not null comment '文物名称',
    type        varchar(50)                               null comment '文物类型(标签)',
    description text                                      null comment '文物介绍',
    size        text                                      null comment '文物尺寸',
    matrials    varchar(50)                               null comment '文物材料',
    dynasty     varchar(32)                               null comment '文物年代',
    likes_count bigint unsigned default '0'               null comment '点赞数',
    views_count bigint unsigned default '0'               null comment '阅读量',
    author      varchar(50)                               null,
    entry_time  int                                       null comment '入馆时间（年份，负数为公元前）',
    create_time datetime        default CURRENT_TIMESTAMP null comment '记录创建时间',
    update_time datetime        default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '记录更新时间'
)
    comment '文物表' charset = utf8mb4;

create index idx_museum_id
    on cultural_relic (museum_id);


