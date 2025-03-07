import os
import math
import datetime
import string as _string
import random as _random
import peewee as pw
from playhouse.shortcuts import model_to_dict, dict_to_model
from season.util.std import stdClass

class Model:
    def __init__(self, tablename=None):
        self.tablename = tablename
        self.orm = wiz.model(f"orm/{tablename}")
        
    @classmethod
    def use(cls, tablename=None):
        return cls(tablename=tablename)

    @staticmethod
    def random(length=16, number=False):
        string_pool = _string.ascii_letters + _string.digits
        if number:
            string_pool = _string.digits
        result = ""
        for i in range(length):
            result += _random.choice(string_pool)
        return result.lower()

    def field(self, key):
        db = self.orm
        return getattr(db, key)

    def create(self):
        self.orm.create_table()

    def get(self, **kwargs):
        kwargs['page'] = 1
        kwargs['dump'] = 1
        data = self.rows(**kwargs)
        if len(data) > 0:
            # return season.stdClass(data[0])
            return stdClass(data[0])

    def count(self, groupby=None, like=None, **where):
        db = self.orm
        try:
            query = db.select(pw.fn.COUNT(db.id).alias("cnt"))
            if like is not None:
                like = like.split(",")
            
            for key in where:
                try:
                    field = getattr(db, key)
                    values = [where[key]]
                    if type(where[key]) == list:
                        values = where[key]

                    qo = None
                    for v in values:
                        if qo is None:
                            if like is not None and key in like:
                                qo = field.contains(v)
                            else:
                                qo = field==v
                        else:
                            if like is not None and key in like:
                                qo = (qo) | (field.contains(v))
                            else:
                                qo = (qo) | (field==v)
                    query = query.where(qo)
                except Exception as e:
                    pass
            
            if groupby is not None:
                groupby = groupby.split(",")
                for i in range(len(groupby)):
                    field = groupby[i]
                    try:
                        field = getattr(db, field)
                        groupby[i] = field
                    except:
                        pass
                query = query.group_by(*groupby)
            
                return len(query)
            
            return query.dicts()[0]['cnt']
        except:
            pass
        return None

    def rows(self, query=None, groupby=None, order='ASC', orderby=None, page=None, dump=10, fields=None, like=None, **where):
        db = self.orm
        if query is None:
            query = db.select()

        if like is not None:
            like = like.split(",")
        for key in where:
            try:
                field = getattr(db, key)
                values = [where[key]]
                if type(where[key]) == list:
                    values = where[key]

                qo = None
                for v in values:
                    if qo is None:
                        if like is not None and key in like:
                            qo = field.contains(v)
                        else:
                            qo = field==v
                    else:
                        if like is not None and key in like:
                            qo = (qo) | (field.contains(v))
                        else:
                            qo = (qo) | (field==v)
                query = query.where(qo)
            except Exception as e:
                pass

        if groupby is not None:
            groupby = groupby.split(",")
            for i in range(len(groupby)):
                field = groupby[i]
                try:
                    field = getattr(db, field)
                    groupby[i] = field
                except:
                    pass
            query = query.group_by(*groupby)

        if orderby is not None:
            orderby = orderby.split(",")
            for i in range(len(orderby)):
                field = orderby[i]
                try:
                    field = getattr(db, field)
                    if order == 'DESC':
                        orderby[i] = field.desc()
                    else:
                        orderby[i] = field
                except:
                    pass
            query = query.order_by(*orderby)

        if page is not None:
            query = query.paginate(page, dump)
        rows = []
        if fields is not None:
            fields = fields.split(",")

        for row in query.dicts():
            if fields is not None:
                obj = dict()
                for field in fields:
                    if field in row:
                        obj[field] = row[field]
                rows.append(obj)
            else:
                rows.append(row)

        return rows

    def facet_rows(self, facet=None, query=None, groupby=None, order='ASC', orderby=None, page=None, dump=10, fields=None, like=None, limit=None, **where):
        db = self.orm
        if query is None:
            query = db.select()

        if facet is not None:
            facet = getattr(db, facet)
            query = db.select(facet.alias("name"), pw.fn.COUNT(facet).alias("cnt"))

        if like is not None:
            like = like.split(",")

        for key in where:
            try:
                field = getattr(db, key)
                values = [where[key]]
                if type(where[key]) == list:
                    values = where[key]

                qo = None
                for v in values:
                    if qo is None:
                        if like is not None and key in like:
                            qo = field.contains(v)
                        else:
                            qo = field==v
                    else:
                        if like is not None and key in like:
                            qo = (qo) | (field.contains(v))
                        else:
                            qo = (qo) | (field==v)

                query = query.where(qo | qo)

            except Exception as e:
                pass
        
        if groupby is not None:
            groupby = groupby.split(",")
            for i in range(len(groupby)):
                field = groupby[i]
                try:
                    field = getattr(db, field)
                    groupby[i] = field
                except:
                    pass
            query = query.group_by(*groupby)

        if orderby is not None:
            orderby = orderby.split(",")
            for i in range(len(orderby)):
                field = orderby[i]
                try:
                    field = getattr(db, field)

                    orderby[i] = field
                    if facet is not None:
                        if order == 'DESC':
                            orderby[i] = pw.fn.COUNT(facet).desc()
                    else:
                        if order == 'DESC':
                            orderby[i] = field.desc()
                    # if order == 'DESC':
                    #     orderby[i] = field.desc()
                    # else:
                    #     orderby[i] = field
                        
                except:
                    pass
            query = query.order_by(*orderby)

        if limit is not None:
            query = query.limit(limit)
        
        if page is not None:
            query = query.paginate(page, dump)
        rows = []

        if fields is not None:
            fields = fields.split(",")

        for row in query.dicts():
            if fields is not None:
                obj = dict()
                for field in fields:
                    if field in row:
                        obj[field] = row[field]
                rows.append(obj)
            else:
                rows.append(row)
        # print(query)
        return rows
        
    def insert(self, *args, **data):
        if len(args) > 0: data = args[0]
        db = self.orm
        if 'id' not in data:
            obj_id = self.random(32)
            while self.get(id=obj_id) is not None:
                obj_id = self.random(32)
            data['id'] = obj_id
        else:
            obj_id = data['id']
        if self.get(id=obj_id) is not None:
            raise Exception("wizdb Error: Duplicated")
        db.create(**data)
        return obj_id

    def update(self, data, **where):
        db = self.orm
        item = dict()
        for key in data:
            if hasattr(db, key):
                item[key] = data[key]
        
        query = db.update(**item)
        for key in where:
            field = getattr(db, key)
            query = query.where(field==where[key])
        query.execute()
        
    def delete(self, **where):
        db = self.orm
        query = db.delete()
        for key in where:
            field = getattr(db, key)
            query = query.where(field==where[key])
        query.execute()
    
    def upsert(self, data, keys="id"):
        keys = keys.split(",")
        wheres = dict()
        for key in keys:
            wheres[key] = data[key]
        check = self.get(**wheres)
        if check is not None:
            self.update(data, **wheres)
        else:
            self.insert(data)

    def upsert_log(self, namespace, timecheck=0):
        try:
            result = self.random(18)

            if not wiz.session.get('SF_SESSION_ID'):
                sid = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + result
                # wiz.session.set('SF_SESSION_ID', sid)
            else:
                sid = wiz.session.get('SF_SESSION_ID')

            if timecheck > 0:
                cnt = self.count(session_id=sid, namespace=namespace, where=f"`accesstime` >= DATE_SUB(now(), INTERVAL {timecheck} HOUR)")
                if cnt > 0: return False, "CHECKED"

            values = dict()
            values['namespace'] = namespace
            values['session_id'] = sid
            values['user_id'] = "undefined"
            values['useragent'] = wiz.request.request().user_agent.string
            values['access_ip'] = wiz.request.ip()
            values['access_time'] = datetime.datetime.now()
            values['full_url'] = wiz.request.uri()

            if wiz.session.get('id'): values['user_id'] = wiz.session.get('id')

            status = self.upsert(values, keys='session_id,user_id,namespace,full_url,access_ip,access_time,useragent')

            return status
        
        except Exception as e:
            return False, e
    
    def search_log(self, text):
        try:
            values = dict()
            values['user_id'] = "undefined"
            values['search_ip'] = wiz.request.ip()
            values['search_text'] = text

            wiz.session = wiz.model("session").use()
            if wiz.session.get('id'): values['user_id'] = wiz.session.get('id')

            keys = "user_id,search_ip,search_text"
            keys = keys.split(",")
            wheres = dict()
            for key in keys:
                wheres[key] = values[key]
            self.insert(values)

            return True
        
        except Exception as e:
            return False, e
