import holidays

# 创建中国大陆节假日对象
cn_holidays = holidays.China()


def is_holiday(date):
    """
    判断某个日期是否是中国大陆的节假日
    :param date: datetime.date 对象或字符串（格式为 YYYY-MM-DD）
    :return: 如果是节假日，返回 True；否则返回 False
    """
    if isinstance(date, str):
        from datetime import datetime

        date = datetime.strptime(date, "%Y-%m-%d").date()

    return date in cn_holidays


# 测试
test_date = "2025-01-01"  # 元旦
if is_holiday(test_date):
    print(f"{test_date} 是中国大陆节假日：{cn_holidays[test_date]}")
else:
    print(f"{test_date} 不是中国大陆节假日")

import datetime

n = datetime.date(2024, 9, 1)
for i in range(365):
    print(
        is_holiday(n + datetime.timedelta(days=i + 1)),
        n + datetime.timedelta(days=i + 1),
    )
