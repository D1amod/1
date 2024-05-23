# coding:utf-8
__author__ = "ila"

import logging, os, xlrd, json, datetime
from flask import request, jsonify,session
from sqlalchemy.sql import func,and_,or_
from api.models.brush_model import *
from . import main_bp
from utils.codes import *
from utils.jwt_auth import Auth
from configs import configs
from utils.helper import *
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from utils.baidubce_api import BaiDuBce
from api.models.config_model import config





# 注册接口
@main_bp.route("/pythone1511/forum/register", methods=['POST'])
def pythone1511_forum_register():
    if request.method == 'POST':
        msg = {'code': normal_code, 'message': 'success', 'data': [{}]}
        req_dict = session.get("req_dict")


        error = forum.createbyreq(forum, forum, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = "注册用户已存在"
        return jsonify(msg)

# 登录接口
@main_bp.route("/pythone1511/forum/login", methods=['GET','POST'])
def pythone1511_forum_login():
    if request.method == 'GET' or request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        req_model = session.get("req_dict")
        try:
            del req_model['role']
        except:
            pass


        datas = forum.getbyparams(forum, forum, req_model)
        if not datas:
            msg['code'] = password_error_code
            msg['msg']='密码错误或用户不存在'
            return jsonify(msg)


        req_dict['id'] = datas[0].get('id')
        return Auth.authenticate(Auth, forum, req_dict)


# 登出接口
@main_bp.route("/pythone1511/forum/logout", methods=['POST'])
def pythone1511_forum_logout():
    if request.method == 'POST':
        msg = {
            "msg": "退出成功",
            "code": 0
        }
        req_dict = session.get("req_dict")

        return jsonify(msg)

# 重置密码接口
@main_bp.route("/pythone1511/forum/resetPass", methods=['POST'])
def pythone1511_forum_resetpass():
    '''
    '''
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success"}

        req_dict = session.get("req_dict")

        if req_dict.get('mima') != None:
            req_dict['mima'] = '123456'

        error = forum.updatebyparams(forum, forum, req_dict)

        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['msg'] = '密码已重置为：123456'
        return jsonify(msg)

# 获取会话信息接口
@main_bp.route("/pythone1511/forum/session", methods=['GET'])
def pythone1511_forum_session():
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "data": {}}
        req_dict={"id":session.get('params').get("id")}
        msg['data']  = forum.getbyparams(forum, forum, req_dict)[0]

        return jsonify(msg)

# 分类接口（后端）
@main_bp.route("/pythone1511/forum/page", methods=['GET'])
def pythone1511_forum_page():
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = session.get("req_dict")
        userinfo = session.get("params")

        try:
            __hasMessage__=forum.__hasMessage__
        except:
            __hasMessage__=None
        if __hasMessage__ and __hasMessage__!="否":
            tablename=session.get("tablename")
            if tablename!="users" and session.get("params")!=None and forum!='chat':
                req_dict["userid"]=session.get("params").get("id")

        tablename=session.get("tablename")
        if tablename=="users" :
            try:
                pass
            except:
                pass
        else:
            mapping_str_to_object = {}
            for model in Base_model._decl_class_registry.values():
                if hasattr(model, '__tablename__'):
                    mapping_str_to_object[model.__tablename__] = model

            try:
                __isAdmin__=mapping_str_to_object[tablename].__isAdmin__
            except:
                __isAdmin__=None

            if __isAdmin__!="是" and session.get("params")!=None:
                req_dict["userid"]=session.get("params").get("id")
            else:
                try:
                    del req_dict["userid"]
                except:
                    pass


        clause_args = []
        or_clauses = or_(*clause_args)

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = forum.page(forum, forum, req_dict, or_clauses)

        return jsonify(msg)

# 排序接口
@main_bp.route("/pythone1511/forum/autoSort", methods=['GET'])
def pythone1511_forum_autosort():
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = session.get("req_dict")
        req_dict['sort']='clicktime'
        req_dict['order']='desc'

        try:
            __browseClick__= forum.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__ =='是':
            req_dict['sort']='clicknum'
        elif __browseClick__ =='时长':
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = forum.page(forum, forum, req_dict)

        return jsonify(msg)

# 分页接口（前端）
@main_bp.route("/pythone1511/forum/list", methods=['GET'])
def pythone1511_forum_list():
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = session.get("req_dict")
        if req_dict.__contains__('vipread'):
            del req_dict['vipread']
            
        userinfo = session.get("params")

        try:
            __foreEndList__=forum.__foreEndList__
        except:
            __foreEndList__=None

        if __foreEndList__ and __foreEndList__!="否":
            tablename=session.get("tablename")
            if tablename!="users" and session.get("params")!=None:
                req_dict['userid']=session.get("params").get("id")

        try:
            __foreEndListAuth__=forum.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users" and session.get("params")!=None:
                req_dict['userid']=session.get("params").get("id")

        tablename=session.get("tablename")
        if tablename=="users" :
            try:
                del req_dict["userid"]
            except:
                pass
        else:
            mapping_str_to_object = {}
            for model in Base_model._decl_class_registry.values():
                if hasattr(model, '__tablename__'):
                    mapping_str_to_object[model.__tablename__] = model

            try:
                __isAdmin__=mapping_str_to_object[tablename].__isAdmin__
            except:
                __isAdmin__=None

            if __isAdmin__!="是" and session.get("params")!=None:
                req_dict["userid"]=session.get("params").get("id")
            else:
                try:
                    del req_dict["userid"]
                except:
                    pass

        if 'luntan' in 'forum':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]


    	


        if 'discuss' in 'forum':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = forum.page(forum, forum, req_dict)

        return jsonify(msg)

# 保存接口（后端）
@main_bp.route("/pythone1511/forum/save", methods=['POST'])
def pythone1511_forum_save():
    '''
    '''
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        for key in req_dict:
            if req_dict[key] == '':
                req_dict[key] = None
        error= forum.createbyreq(forum, forum, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 添加接口（前端）
@main_bp.route("/pythone1511/forum/add", methods=['POST'])
def pythone1511_forum_add():
    '''
    '''
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        try:
            __foreEndListAuth__=forum.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users":
                req_dict['userid']=session.get("params").get("id")
            
        error= forum.createbyreq(forum, forum, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 踩、赞接口
@main_bp.route("/pythone1511/forum/thumbsup/<id_>", methods=['GET'])
def pythone1511_forum_thumbsup(id_):
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        rets=forum.getbyid(forum, forum,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = forum.updatebyparams(forum, forum, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 获取详情信息（后端）
@main_bp.route("/pythone1511/forum/info/<id_>", methods=['GET'])
def pythone1511_forum_info(id_):
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}

        data = forum.getbyid(forum, forum, int(id_))
        if len(data)>0:
            msg['data']=data[0]
        #浏览点击次数
        try:
            __browseClick__= forum.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__  and  "clicknum"  in forum.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}
            ret=forum.updatebyparams(forum,forum,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 获取详情信息（前端）
@main_bp.route("/pythone1511/forum/detail/<id_>", methods=['GET'])
def pythone1511_forum_detail(id_):
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}

        data = forum.getbyid(forum, forum, int(id_))
        if len(data)>0:
            msg['data']=data[0]

        #浏览点击次数
        try:
            __browseClick__= forum.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__   and  "clicknum"  in forum.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}
            ret=forum.updatebyparams(forum,forum,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 更新接口
@main_bp.route("/pythone1511/forum/update", methods=['POST'])
def pythone1511_forum_update():
    '''
    '''
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        if req_dict.get("mima") and "mima" not in forum.__table__.columns :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in forum.__table__.columns :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass


        error = forum.updatebyparams(forum, forum, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 删除接口
@main_bp.route("/pythone1511/forum/delete", methods=['POST'])
def pythone1511_forum_delete():
    '''
    '''
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")

        error=forum.delete(
            forum,
            req_dict
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 投票接口
@main_bp.route("/pythone1511/forum/vote/<int:id_>", methods=['POST'])
def pythone1511_forum_vote(id_):
    '''
    '''
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success"}


        data= forum.getbyid(forum, forum, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=forum.updatebyparams(forum,forum,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return jsonify(msg)

@main_bp.route("/pythone1511/forum/flist", methods=['GET'])
def pythone1511_forum_flist():
    '''
    查看所有开放的帖列表(无需登录)
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = session.get("req_dict")

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize'] = forum.page(forum, forum, req_dict)

        return jsonify(msg)


        return jsonify(msg)


@main_bp.route("/pythone1511/forum/list/<id_>", methods=['GET'])
def pythone1511_forum_list_id(id_):
    '''
    查看主贴和所有回帖内容(无需登录)
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {"currPage":1,"totalPage":1,"total":1,"pageSize":10,"childs":[]}}

        params = {"id":id_}

        datas = forum.retrieve(forum, forum)


        current_id=0#当前id，也就是parent_id,找到了下一级，把下一级id赋值给current_id，当做下下一级id的paretn_id
        for i in datas:
            if i.get('id')==params.get('id'):
                current_id=i.get('id')
                msg['data'].update(i)

        #循环记录count长度的数字，每次把当前id赋值给current_id
        for i in range(len(datas)):
            for i in datas:
                if i.get('parentid')==current_id:
                    msg['data']["childs"].append(i)
                    current_id=i.get("id")
                    break


        return jsonify(msg)





# 分组统计接口
@main_bp.route("/pythone1511/forum/group/<columnName>", methods=['GET'])
def pythone1511_forum_group(columnName):
    '''
    分组统计接口
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        userinfo = session.get("params")


        msg['data'] = forum.groupbycolumnname(forum,forum,columnName,req_dict)
        msg['data'] = msg['data'][:10]
        return jsonify(msg)

# 按值统计接口
@main_bp.route("/pythone1511/forum/value/<xColumnName>/<yColumnName>", methods=['GET'])
def pythone1511_forum_value(xColumnName, yColumnName):
    '''
    按值统计接口,
    {
        "code": 0,
        "data": [
            {
                "total": 10.0,
                "shangpinleibie": "aa"
            },
            {
                "total": 20.0,
                "shangpinleibie": "bb"
            },
            {
                "total": 15.0,
                "shangpinleibie": "cc"
            }
        ]
    }
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        userinfo = session.get("params")


        msg['data'] = forum.getvaluebyxycolumnname(forum,forum,xColumnName,yColumnName,req_dict)
        msg['data'] = msg['data'][:10]
        return jsonify(msg)

# 按日期统计接口
@main_bp.route("/pythone1511/forum/value/<xColumnName>/<yColumnName>/<timeStatType>", methods=['GET'])
def pythone1511_forum_value_riqi(xColumnName, yColumnName, timeStatType):
    '''
    按日期统计接口
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}

        where = ' where 1 = 1 '

        sql = ''
        if timeStatType == '日':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM forum {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d')".format(xColumnName, yColumnName, where, '%Y-%m-%d')

        if timeStatType == '月':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM forum {2} GROUP BY DATE_FORMAT({0}, '%Y-%m')".format(xColumnName, yColumnName, where, '%Y-%m')

        if timeStatType == '年':
            sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM forum {2} GROUP BY DATE_FORMAT({0}, '%Y')".format(xColumnName, yColumnName, where, '%Y')

        data = db.session.execute(sql)
        data = data.fetchall()
        results = []
        for i in range(len(data)):
            result = {
                xColumnName: decimalEncoder(data[i][0]),
                'total': decimalEncoder(data[i][1])
            }
            results.append(result)
            
        msg['data'] = results
        return jsonify(msg)

# 推荐算法接口
@main_bp.route("/pythone1511/forum/autoSort2", methods=['GET'])
def pythone1511_forum_autoSort2():
    if request.method == 'GET':

        leixing = set()
        req_dict = session.get("req_dict")
        userinfo = session.get("params")
        sql = "select inteltype from storeup where userid = "+userinfo.get("id")+" and tablename = 'forum' order by addtime desc"
        try:
            data = db.session.execute(sql)
            rows = data.fetchall()
            for row in rows:
                for item in row:
                    if item != None:
                        leixing.add(item)
        except:
            leixing = set()

        L = []
        sql ="select * from forum where $intelRecomColumn in ('%s"%("','").join(leixing)+"') union all select * from forum where $intelRecomColumn not in('%s"%("','").join(leixing)+"')"
        data = db.session.execute(sql)
        data_dict = [dict(zip(result.keys(), result)) for result in data.fetchall()]
        for online_dict in data_dict:
            for key in online_dict:
                if 'datetime.datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    pass
            L.append(online_dict)

        return jsonify({"code": 0, "msg": '',  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":5,"list": L[0:int(req_dict['limit'])]}})







# 统计接口
@main_bp.route("/pythone1511/forum/remind/<columnName>/<type>", methods=['GET'])  #
def pythone1511_forum_remind(columnName,type):
    '''
    '''
    if request.method == 'GET':
        msg = {"code": normal_code, 'count': 0}
        # 组合查询参数
        params = session.get("req_dict")
        if int(type)==1:#数字
            if params.get('remindstart') == None and params.get('remindend') != None:
                remindstart = 0
                remindend = int(params['remindend'])
            elif params.get('remindstart') != None and params.get('remindend') == None:
                remindstart = int(params['remindstart'])
                remindend = 999999
            elif params.get('remindstart') == None and params.get('remindend') == None:
                remindstart = 0
                remindend = 999999
        elif int(type)==2:#日期
            current_time=int(time.time())
            if params.get('remindstart') == None and params.get('remindend') != None:
                starttime=current_time-60*60*24*365*2
                params['remindstart'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
                endtime=current_time+60*60*24*params.get('remindend')
                params['remindend'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))

            elif params.get('remindstart') != None and params.get('remindend') == None:
                starttime= current_time - 60 * 60 * 24 * params.get('remindstart')
                params['remindstart']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
                endtime=current_time+60*60*24*365*2
                params['remindend'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))
            elif params.get('remindstart') == None and params.get('remindend') == None:
                starttime = current_time - 60 * 60 * 24 * 365 * 2
                params['remindstart'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
                endtime = current_time + 60 * 60 * 24 * 365 * 2
                params['remindend'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))

        data = forum.getbetweenparams(
            forum,
            forum,
            columnName,
            {
                "remindStart": remindstart,
                "remindEnd": remindend
            }
        )

        msg['count'] = len(data)
        return jsonify(msg)




