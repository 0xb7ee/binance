vol_1w_std  prc_1w_std  vol_2w_std  prc_2w_std

CREATE TABLE IF NOT EXISTS `binance_vp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(12) NOT NULL DEFAULT '' COMMENT '交易对',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '4h K线时间',
  `vol_1w_std` float NOT NULL COMMENT '当前K线的交易量是一周交易量均值的多少倍标准差',
  `prc_1w_std` float NOT NULL COMMENT '当前K线的收盘价是一周收盘价均值的多少倍标准差',
  `vol_2w_std` float NOT NULL COMMENT '当前K线的交易量是两周交易量均值的多少倍标准差',
  `prc_2w_std` float NOT NULL COMMENT '当前K线的收盘价是两周收盘价均值的多少倍标准差',
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_key` (`key`),
  KEY `idx_time` (`time`),
  KEY `idx_uptime` (`update_time`),
  KEY `idx_createtime` (`create_time`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='币安交易对量价表' AUTO_INCREMENT=0 ;