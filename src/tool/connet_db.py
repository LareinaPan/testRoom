import logging
import pymysql
from pymongo import MongoClient
import pymongo
from bson import ObjectId


def op_db_query(sql, host, user, password, database):
    """
    不需要跳板机，连接mysql
    :param sql: 需要执行的命令
    :param host: 机器地址
    :param user: sql登陆用户
    :param password: sql登陆密码
    :param db: 需要连接的数据库
    :return: 查询结果，以元组的形式
    """
    db_res = pymysql.connect(host=host, user=user, password=password, database=database, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db_res.cursor()
    try:
        cur.execute(sql) # 执行sql语句
        results = cur.fetchall() # 获取查询的所有记录
        logging.info("查询条件==>{}".format(sql))
        logging.info("查询结果==>{}".format(results))
        return results
    except Exception as e:
        logging.error("查询异常==>{}".format(e))

    finally:
        db_res.close()


def op_db_modify(sql, host, user, password, database):
    """
    不需要跳板机，连接mysql
    :param sql: 需要执行的命令
    :param host: 机器地址
    :param user: sql登陆用户
    :param password: sql登陆密码
    :param db: 需要连接的数据库
    :return: 查询结果，以元组的形式
    """
    db_res = pymysql.connect(host=host, user=user, password=password, database=database, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db_res.cursor()
    try:
        cur.execute(sql) # 执行sql语句
        logging.info("执行语句==>{}".format(sql))
        db_res.commit()

    except Exception as e:
        logging.error("sql执行异常==>{}".format(e))
        db_res.rollback()

    finally:
        db_res.close()

class OperateMongo:
    def __init__(self, mongo):
        password = None
        user = None
        if mongo == 'te':
            self.mongo = ['mgd1app.te.test.srv.mc.dd:27017', 'mgd2app.te.test.srv.mc.dd:27017',
                          'mgd3app.te.test.srv.mc.dd:27017']
        elif mongo == 'te_promote_sales':
            self.mongo = ['10.23.34.29:27017', '10.23.34.30:27017', '10.23.34.39:27017']
            password = '98LbbHSYwE2z'
            user = 'mongouser'

        self.client = MongoClient(self.mongo) #连接数据库
        if user is not None:
            self.adAdmin = self.client.admin
            self.adAdmin.authenticate(user, password)

    # 查询,默认按_id倒序排
    def select_mongo_data(self, db_name, collect_name, condition_map, paraName):
        """
        :param db_name: 数据库名
        :param collect_name: 数据表名
        :param condition_map: 查询的条件
        :param paraName: 查询返回指定的一个字段
        :return:
        """
        db = self.client[db_name]
        collection = db[collect_name]
        results = collection.find(condition_map).sort('_id', pymongo.DESCENDING)
        result_list = []
        print("results:", results)
        for result in results:
            print(result)
            data = result[paraName]
            result_list.append(data)

        if len(result_list) == 0:
            return None
        else:
            return result_list

    # 查询,默认按_id倒序排
    def select_mongo_data2(self, db_name, collect_name, query, projection, skip_number=0,
                       limit_number=0, sort_field='_id', order=-1, is_sort=1):
        """
        查询mongo,默认按照updata_time字段倒序排序多条件情况
        :param db_name: 连接的数据库
        :param collect_name: 数据库对应的表
        :param query: 查询条件
        :param projection: 查询后返回字段,如:{"_id":1, "name":1};1展示,0不展示
        :param skip_number: 数据库对应的表
        :param limit_number: 返回记录中跳过几条数据后再返回
        :param sort_field: 排序的字段
        :param order: 排序方式,-1倒序
        :param is_sort: 是否需要排序:0不排,1排
        :return:
        """

        collection = self.client[db_name][collect_name]
        result_list = []
        if is_sort ==1:# 排序
            results = collection.find(query, projection).limit(limit_number).skip(skip_number).sort(sort_field, order)
        elif is_sort ==0:#不排序
            results = collection.find(query, projection).limit(limit_number).skip(skip_number)

        for result in results:
            print(result)
            result_list.append(result)

        if len(result_list) == 0:
            return None
        else:
            return result_list

    # 查询,默认按_id倒序排
    def select_mongo_by_id(self, db_name, collect_name, condition_map):

        db = self.client[db_name]
        collection = db[collect_name]
        results = collection.find(condition_map).sort('_id', pymongo.DESCENDING)
        result = []
        try:
            if results and len(result):
                result = results[0]
        except pymongo.errors.PyMongoError as e:
            print("没查询到数据")
        return result

    # 更新数据库
    def updata_mongo_data(self, db_name, collect_name, myrequireinfo, condition_map):
        try:
            collection = self.client[db_name][collect_name]
            results = collection.updata_one(myrequireinfo, condition_map)
            return results
        except pymongo.errors.PyMongoError as e:
            print("DB Error==>{}".format(e))

    # 插入数据库
    def insert_mongo_data(self, db_name, collect_name, document):
        try:
            collection = self.client[db_name][collect_name]
            results = collection.insert_one(document)
            return results
        except pymongo.errors.PyMongoError as e:
            print("DB Error==>{}".format(e))

    # 删除数据库数据
    def delete_mongo_data(self, db_name, collect_name, condition_map):
        try:
            collection = self.client[db_name][collect_name]
            results = collection.delete_many(condition_map)
            return results
        except pymongo.errors.PyMongoError as e:
            print("DB Error==>{}".format(e))


if __name__ == "__main__":
    db = OperateMongo('te_user')
    db_result = db.select_mongo_data2("area", "user", {"_id": ObjectId("6123")}, {"mobile": 1})