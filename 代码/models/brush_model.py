# coding:utf-8
import random
from datetime import datetime
from sqlalchemy import text,TIMESTAMP

from api.models.models import Base_model
from api.exts import db
from sqlalchemy.dialects.mysql import DOUBLE,LONGTEXT
# 个人信息
class yonghu(Base_model):
    __doc__ = u'''yonghu'''
    __tablename__ = 'yonghu'

    __loginUser__='yonghuzhanghao'


    __authTables__={}
    __authPeople__='是'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='否'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    yonghuzhanghao=db.Column( db.VARCHAR(255), nullable=False,unique=True,comment='用户账号' )
    mima=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='密码' )
    yonghuxingming=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='用户姓名' )
    xingbie=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='性别' )
    lianxifangshi=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='联系方式' )
    touxiang=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )


class zufangxinxi(Base_model):
    __doc__ = u'''zufangxinxi'''
    __tablename__ = 'zufangxinxi'



    __authTables__={}
    __authPeople__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='是'
    __browseClick__='是'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    laiyuan=db.Column( db.Text,  nullable=True, unique=False,comment='来源' )
    fengmian=db.Column( db.Text,  nullable=True, unique=False,comment='封面' )
    biaoti=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='标题' )
    yuezu=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='月租' )
    huxing=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='户型' )
    louceng=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='楼层' )
    mianji=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='面积' )
    zhuangxiu=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='装修' )
    chaoxiang=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='朝向' )
    xiaoqu=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='小区' )
    xiangqing=db.Column( db.Text,  nullable=True, unique=False,comment='详情' )
    clicktime=db.Column( db.DateTime,  nullable=True, unique=False,comment='最近点击时间' )
    clicknum=db.Column( db.Integer,default=0,  nullable=True, unique=False,comment='点击次数' )


class forum(Base_model):
    __doc__ = u'''forum'''
    __tablename__ = 'forum'



    __authTables__={}
    __foreEndListAuth__='是'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    title=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='帖子标题' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='帖子内容' )
    parentid=db.Column( db.BigInteger,  nullable=True, unique=False,comment='父节点id' )
    userid=db.Column( db.BigInteger, nullable=False, unique=False,comment='用户id' )
    username=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='用户名' )
    avatarurl=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )
    isdone=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='状态' )


class news(Base_model):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    title=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='标题' )
    introduction=db.Column( db.Text,  nullable=True, unique=False,comment='简介' )
    picture=db.Column( db.Text, nullable=False, unique=False,comment='图片' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='内容' )


class aboutus(Base_model):
    __doc__ = u'''aboutus'''
    __tablename__ = 'aboutus'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    title=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='标题' )
    subtitle=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='副标题' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='内容' )
    picture1=db.Column( db.Text,  nullable=True, unique=False,comment='图片1' )
    picture2=db.Column( db.Text,  nullable=True, unique=False,comment='图片2' )
    picture3=db.Column( db.Text,  nullable=True, unique=False,comment='图片3' )


class systemintro(Base_model):
    __doc__ = u'''systemintro'''
    __tablename__ = 'systemintro'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    title=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='标题' )
    subtitle=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='副标题' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='内容' )
    picture1=db.Column( db.Text,  nullable=True, unique=False,comment='图片1' )
    picture2=db.Column( db.Text,  nullable=True, unique=False,comment='图片2' )
    picture3=db.Column( db.Text,  nullable=True, unique=False,comment='图片3' )


