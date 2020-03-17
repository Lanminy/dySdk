#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from pymongo.collection import Collection

from settings import settings

host = settings.MONGO_HOST
port = settings.MONGO_PORT

client = pymongo.MongoClient(host=host, port=port)
db = client['douyin']


def handle_init_task():
    """
    初始化任务, 向MongoDB添加任务id
    :return:
    """
    task_id_collection = Collection(db, 'task_id')

    with open('douyin_hot_id.txt', 'r') as f_share:
        for f_share_task in f_share.readlines():
            init_task = {}
            init_task['share_id'] = f_share_task.replace('\n', '')
            print(init_task)
            task_id_collection.insert(init_task)


def handle_get_task():
    task_id_collection = Collection(db, 'task_id')
    task = task_id_collection.find_one_and_delete({})
    return task


# handle_init_task()

handle_get_task()