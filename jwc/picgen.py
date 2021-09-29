# 图片生成


from model.course import Course
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from jwc.config import *
import datetime


def get_dow_name(i: int):
    DOW_LIST = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
    return DOW_LIST[i]


def dow2order(i: int):
    DOW_ORDER_LIST = [7, 1, 2, 3, 4, 5, 6]
    return DOW_ORDER_LIST[i]


def get_date(week: int, dow_order: int):
    target_date = DAY_BASE + (week - 1) * WEEK_SPAN + dow_order * DAY_SPAN
    return "{}-{}".format(target_date.month, target_date.day)


# 将一段文字 每隔n个字符插入一个换行符
def text_format(s: str, n: int):
    cnt = len(s) // n
    ls = []
    i = 0
    for i in range(cnt):
        ls.append(s[i * n : (i + 1) * n])
        i += 1
    ls.append(s[i * n :])
    return "\n".join(ls)


# 获取颜色:
def get_color(i: int):
    color_ls = [
        (2, 195, 154),
        (231, 29, 54),
        (168, 218, 220),
        (69, 123, 157),
        (255, 107, 107),
        (244, 162, 97),
        (91, 192, 235),
    ]
    return color_ls[i]


def draw_topbar(draw: ImageDraw, week_order: int):
    font = ImageFont.truetype(FONT_TYPE, TOPBAR_FONT_SIZE)
    dow = 1
    x0 = MARGIN_LEFT
    y0 = 0
    for dow_order in range(1, 8):
        draw.text(
            (x0 + DOW_BASE[0], y0 + DOW_BASE[1]),
            get_dow_name(dow),
            font=font,
            fill=(0, 0, 0),
        )
        draw.text(
            (x0 + DATE_BASE[0], y0 + DATE_BASE[1]),
            get_date(week_order, dow_order),
            font=font,
            fill=(0, 0, 0),
        )
        x0 += COURSEBOX_WIDTH
        dow = (dow + 1) % 7


# 获取要绘制的课表格子的坐标
def get_box_coordinate(
    dayOfWeek: int, startSection: int, endSection: int
) -> Tuple[int, int, int, int]:
    # 周日为 0 所以做 (dayOfWeek + 6) // 7 处理
    x0 = MARGIN_LEFT + COURSEBOX_WIDTH * ((dayOfWeek + 6) % 7)
    y0 = MARGIN_TOP + TOPBAR_HEIGHT + COURSEBOX_HEIGHT * (startSection - 1)
    x1 = x0 + COURSEBOX_WIDTH
    y1 = y0 + (endSection - startSection + 1) * COURSEBOX_HEIGHT
    # 课表格子间取间距
    x0 += COURSE_MARGIN
    y0 += COURSE_MARGIN
    x1 -= COURSE_MARGIN
    y1 -= COURSE_MARGIN
    return (x0, y0, x1, y1)


# 绘制某个课表格子 起始点 (x,y) 结束点 (x,y)
def draw_box(draw: ImageDraw, xy: Tuple[int, int, int, int], course: Course):
    font = ImageFont.truetype(FONT_TYPE, FONT_SIZE)
    draw.rounded_rectangle(
        xy=xy,
        radius=COURSE_RADIUS,
        outline=(255, 255, 255),
        fill=get_color(course.day_of_week),
        width=2,
    )
    draw.text(
        (xy[0] + COURSE_NAME_BASE[0], xy[1] + COURSE_NAME_BASE[1]),
        text_format(course.name, 4),
        font=font,
    )
    draw.text(
        (xy[0] + COURSE_ROOM_BASE[0], xy[3] + COURSE_ROOM_BASE[1]),
        text_format(course.room, 4),
        font=font,
    )


def draw_all(courses: List[Course], filename: str, week_order: int):
    # 1080 20 + 150 * 7 + 20
    width = MARGIN_LEFT + COURSEBOX_WIDTH * 7 + MARGIN_RIGHT
    # 2340 20 + 170 * 13 + 20
    height = MARGIN_TOP + COURSEBOX_HEIGHT * 13 + MARGIN_BUTTOM

    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw_topbar(draw, week_order)
    for course in courses:
        if course.week_start > week_order or course.week_end < week_order:
            continue
        draw_box(
            draw,
            get_box_coordinate(
                course.day_of_week, course.section_start, course.section_end
            ),
            course,
        )
    image.save("{}{}.jpg".format(COURSE_PIC_SAVE_PATH,filename), "jpeg")
