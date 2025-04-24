import h5py
import rich
import os
import time
import shutil
import T5_a

file_path = "Translate_result_data_2.h5"
backup_dir = "./backup"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)


def key_exs(key):
    with h5py.File(file_path, "a") as f:
        if key in f:
            return True
        return False


def query_key(key):
    """
    :return: value
    """
    with h5py.File(file_path, "a") as f:
        if key in f:
            if isinstance(f[key], h5py.Dataset):
                print("[😄 get:]", str(f[key][()].decode("utf-8")))
                if key == str(f[key][()].decode("utf-8")):
                    rich.print("[😤 warning:]" + f" Indifferent~> {key}")
                return str(f[key][()].decode("utf-8"))
            else:
                return f"[👿 wrong data:] [{key}] is a group, not a dataset."
        else:
            rich.print("[😡 Not exs:]" + f" ~>{key}")
            return key


def add_key_value(key, value):
    with h5py.File(file_path, "a") as f:
        if key not in f:
            f.create_dataset(key, data=value)
        else:
            print(key == value)
            print(f"Key '{key}' already exists.")


def list_all_keys():
    import rich

    with h5py.File(file_path, "r") as f:
        for key in f.keys():
            if isinstance(f[key], h5py.Dataset):
                value = f[key][()]
                value = value.decode("utf-8") if isinstance(value, bytes) else value
                T5_a.add_key_value(key=key, value=value)
                rich.print(f"\n🚀🚀🚀{key}👉👉👉{value}🔥🔥🔥\n")


def list_invalid_keys():
    import rich

    with h5py.File(file_path, "r") as f:
        for key in f.keys():
            if not isinstance(f[key], h5py.Dataset):
                value = "INVALID"
                rich.print(
                    f"\n🚀🚀🚀{key}🧐🧐🧐{value.decode('utf-8') if isinstance(value, bytes) else value}🔥🔥🔥\n"
                )


def delete_invalid_keys():
    shutil.copyfile(src=file_path, dst=os.path.join(backup_dir, f"{time.time()}.h5"))
    with h5py.File(file_path, "a") as f:
        keys_to_delete = [
            key for key in f.keys() if not isinstance(f[key], h5py.Dataset)
        ]

        for key in keys_to_delete:
            del f[key]
            rich.print(f"\n🔥🔥🔥 删除无效键: {key} 🗑️\n")


if __name__ == "__main__":
    # add_key_value('name', '姓名')
    # add_key_value('age', '年龄')
    # add_key_value('Thank you', '谢谢你')
    # print(query_key('你好'))
    # print(query_key('age'))
    # print(query_key('Thank you'))
    # print(query_key('address'))
    list_all_keys()
    # list_invalid_keys()
    # delete_invalid_keys()
