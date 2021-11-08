from pydantic.tools import T
from lib.config import *
import textwrap


def get_weekorder_name(week_order: int):
    dic = {
        1: "第一周",
        2: "第二周",
        3: "第三周",
        4: "第四周",
        5: "第五周",
        6: "第六周",
        7: "第七周",
        8: "第八周",
        9: "第九周",
        10: "第十周",
        11: "第十一周",
        12: "第十二周",
        13: "第十三周",
        14: "第十四周",
        15: "第十五周",
        16: "第十六周",
        17: "第十七周",
        18: "第十八周",
        19: "第十九周",
        20: "第二十周",
    }
    return dic[week_order]


def get_dow_name(i: int):
    DOW_LIST = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
    return DOW_LIST[i]


def dow2order(i: int):
    DOW_ORDER_LIST = [7, 1, 2, 3, 4, 5, 6]
    return DOW_ORDER_LIST[i]


def get_date(week: int, dow_order: int):
    target_date = DAY_ANCHOR + (week - 1) * WEEK_SPAN + dow_order * DAY_SPAN
    return "{}-{}".format(target_date.month, target_date.day)


def name_format(text: str, n: int) -> str:
    return textwrap.fill(text, width=n)


# 获取颜色:
def get_color(i: int):
    color_ls = [
        (255, 168, 64, 255),
        (57, 211, 169, 255),
        (254, 134, 147, 255),
        (111, 137, 226, 255),
        # (239, 130, 109, 255),
        (99, 186, 255, 255),
        (254, 212, 64, 255),
        (184, 150, 230, 255),
        (169, 213, 59, 255),
    ]
    return color_ls[i]
