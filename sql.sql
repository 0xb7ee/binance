CREATE TABLE IF NOT EXISTS `binance_vp`
(
  `id`          int(11)     NOT NULL AUTO_INCREMENT,
  `key`         varchar(12) NOT NULL DEFAULT '' COMMENT '交易对',
  `time`        timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '4小时K线起始时间',
  `close`       float       NOT NULL COMMENT '收盘价',
  `vol_1w_std`  float       NOT NULL COMMENT '一周成交量标准差倍数',
  `prc_1w_std`  float       NOT NULL COMMENT '一周价格标准差倍数',
  `vol_2w_std`  float       NOT NULL COMMENT '两周成交量标准差倍数',
  `prc_2w_std`  float       NOT NULL COMMENT '两周价格标准差倍数',
  `update_time` timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_time` timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_key` (`key`),
  KEY `idx_time` (`time`),
  KEY `idx_uptime` (`update_time`),
  KEY `idx_createtime` (`create_time`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 COMMENT ='币安交易对的量价表'
  AUTO_INCREMENT = 0;

CREATE TABLE IF NOT EXISTS `binance_boll`
(
  `id`          int(11)     NOT NULL AUTO_INCREMENT,
  `key`         varchar(12) NOT NULL DEFAULT '' COMMENT '交易对',
  `time`        timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '4小时K线起始时间',
  `close`       float       NOT NULL COMMENT '收盘价',
  `rate`        float       NOT NULL COMMENT 'boll率',
  `k3up`        float       NOT NULL COMMENT '当前boll上轨与上一个boll上轨比值',
  `k2up`        float       NOT NULL COMMENT '上一个boll上轨与上两个boll上轨比值',
  `k3md`        float       NOT NULL COMMENT '当前boll中轨与上一个boll中轨比值',
  `k2md`        float       NOT NULL COMMENT '上一个boll中轨与上两个boll中轨比值',
  `k3lw`        float       NOT NULL COMMENT '当前boll下轨与上一个boll下轨比值',
  `k2lw`        float       NOT NULL COMMENT '上一个boll下轨与上两个boll下轨比值',
  `update_time` timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_time` timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_key` (`key`),
  KEY `idx_time` (`time`),
  KEY `idx_uptime` (`update_time`),
  KEY `idx_createtime` (`create_time`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 COMMENT ='币安交易对的boll线表'
  AUTO_INCREMENT = 0;