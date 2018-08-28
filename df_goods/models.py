#  coding: utf-8
from __future__ import unicode_literals
from tinymce.models import HTMLField
from django.db import models

# Create your models here.
# 商品分类
class TypeInfo(models.Model):
    #index首页商品分类信息
    ttitle = models.CharField(verbose_name ='类型名称',max_length=20)
    # 是否删除,默认不删
    isDelete = models.BooleanField(verbose_name ='是否删除',default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')
    class Meta:
        verbose_name = '分类信息'
        verbose_name_plural = '分类信息'


class GoodsInfo(models.Model):
    #商品名字
    gtitle = models.CharField(verbose_name ='商品名称',max_length=50)
    # 商品图片位置    服务器部署记得看看
    gpic = models.ImageField(verbose_name ='商品图片',upload_to='df_goods')
    # 商品价格(12.00)
    gprice = models.DecimalField(verbose_name ='商品价格',max_digits=5, decimal_places=2)
    # 物理删除该商品
    isDelete = models.BooleanField(default=False)
    # 单位
    gunit = models.CharField(verbose_name ='商品单位',max_length=20, default='500g')
    # 点击量(销量)  用于排序（减轻服务器的负担）
    gclick = models.IntegerField(verbose_name ='点击量')
    # 商品介绍
    gjianjie = models.CharField(verbose_name ='简介',max_length=300)
    # 库存
    gkucun = models.IntegerField(verbose_name ='库存')
    # 商品的详细介绍　　　　富文本编辑器
    gcontent = HTMLField(verbose_name ='详细介绍',)
    # 商品类型
    gtype = models.ForeignKey(TypeInfo,verbose_name='所属分类', on_delete=models.CASCADE)

    def __str__(self):
        return self.gtitle.encode('utf-8')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'


# TypeInfo_list = TypeInfo.objects.all()
# #伪造数据生成器    可批量造假数据测试
# fake = Factory.create('zh_CN')   
# for i in range(0,300):
#     j = random.randint(0, 100)
#     s1 = random.randint(0, 100)
#     s2 = random.randint(0, 100)
#     k = random.randint(0, 7)
#     v = GoodsInfo(
#         gtitle=fake.text(max_nb_chars=10),
#         gpic='df_goods/goods.jpg',
#         gprice=j,
#         gunit='500g',
#         gclick=0,
#         # isDelete=fake.pybool(),   #是否删除
#         gjianjie=fake.text(max_nb_chars=70),
#         gkucun=s2,
#         gcontent=fake.text(max_nb_chars=300),
#         gtype=TypeInfo_list[k],   #所属类型
#     )
#     v.save()