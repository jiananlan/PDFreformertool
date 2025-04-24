import subprocess
import rich
from pymongo import MongoClient
import Tconfig
import Tremove_markdown


def run_mongo():
    mgdb_path = Tconfig.configuration["mongodb"]
    db_path = Tconfig.configuration["database_path"]
    command = f"{mgdb_path} --dbpath {db_path}"

    try:
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        print("🥭🥭🥭MongoDB 已在后台启动")
    except Exception as ex:
        rich.print(f"🥵🥵🥵[red]启动失败:[/red] {ex}")


run_mongo()

client = MongoClient(Tconfig.configuration["mongo_url"])

db = client["Translater"]
collection = db["trs_2"]
collection.create_index("raw", unique=True)


def key_exs(key):
    results = collection.find({"raw": key})
    try:
        if results:
            if results[0]["get_available"]:
                return True
    except IndexError:
        return False
    return False


def query_key(key):
    results = collection.find({"raw": key})
    try:
        if results[0]["get_available"]:
            r = Tremove_markdown.md_to_text(results[0]["result"])
            if r is not None:
                r = "\n".join(x for x in r.split("\n") if x)
            else:
                r = key
            print("[😄 get:]", r)
            return r
    except IndexError:
        try:
            rich.print("[😡 Not exs:]" + f" ~>{key}")
        except:
            print('rich error')
        return key


def add_key_value(key, value):
    data_ = {
        "raw": key,
        "result": value,
        "get_available": True,
        "trans_available": False,
    }
    try:
        result_ = collection.insert_one(data_)
        print("😉😉😉Inserted ID😉😉😉", result_.inserted_id)
    except Exception as e_:
        print(f"😨😨😨已经存在😨😨😨{e_}")


def find_problem():
    for doc in collection.find({"result": None}):
        print(doc)
    result = collection.delete_many({"result": None})
    print(result)

def remove_illegal():
    for doc in collection.find():
        try:
            l1,l2=list(filter(None,doc['raw'].split('\n'))),list(filter(None,doc['result'].split('\n')))
            if len(l1)-len(l2)<-1:
                print(len(l1),len(l2))
                print(l1,l2,sep='\n')
        except Exception as e:print(e)


if __name__ == "__main__":
    remove_illegal()
    add_key_value("test", "测试")
    query_key("hello  world")
    query_key("hello world")
