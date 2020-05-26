# -
爬虫-包括静态json数据和动态jquery信息的获取



对京东某一个商城的所有商品进行抓取，以纸尿裤（好奇和pampers为例）包括以下几个特征值：
            'name':商城名字
            'wareId':skuid
            'wname':名字
            'detail':名字细节
            'size':大小,
            'number(片)':一份里的数量,
            '最终jdPrice':价格,
            'coupon':优惠券,
            'promotion':促销,
            'quan':促销券,
            'update': 更新日期
##
hearder里需要填入自己的session

##
由于京东优惠券和促销是动态jquery控件加载的，所以通过以下方法获取
https://item.jd.com/coupons?skuId=208399&cat=1319%2C1525%2C7057&venderId=1000001933
https://cd.jd.com/promotion/v2?callback=jQuery8797075&skuId=208399&area=5_239_243_48622&venderId=1000001933&cat=1319%2C1525%2C7057
