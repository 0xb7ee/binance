vol_1w_std  prc_1w_std  vol_2w_std  prc_2w_std

CREATE TABLE IF NOT EXISTS `binance_vp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(12) NOT NULL DEFAULT '' COMMENT '���׶�',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '4h K��ʱ��',
  `vol_1w_std` float NOT NULL COMMENT '��ǰK�ߵĽ�������һ�ܽ�������ֵ�Ķ��ٱ���׼��',
  `prc_1w_std` float NOT NULL COMMENT '��ǰK�ߵ����̼���һ�����̼۾�ֵ�Ķ��ٱ���׼��',
  `vol_2w_std` float NOT NULL COMMENT '��ǰK�ߵĽ����������ܽ�������ֵ�Ķ��ٱ���׼��',
  `prc_2w_std` float NOT NULL COMMENT '��ǰK�ߵ����̼����������̼۾�ֵ�Ķ��ٱ���׼��',
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '�޸�ʱ��',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '����ʱ��',
  PRIMARY KEY (`id`),
  KEY `idx_key` (`key`),
  KEY `idx_time` (`time`),
  KEY `idx_uptime` (`update_time`),
  KEY `idx_createtime` (`create_time`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='�Ұ����׶����۱�' AUTO_INCREMENT=0 ;