# 图片生成


from model.course import Course
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from jwc.config import *
from jwc.util import *


def draw_topbar(draw: ImageDraw.ImageDraw, week_order: int):
    font = ImageFont.truetype(FONT_TYPE, TOPBAR_FONT_SIZE)
    draw.text(
        WEEKORDER_ANCHOR, get_weekorder_name(week_order), font=font, fill=(12, 12, 12)
    )


def draw_weekbar(draw: ImageDraw.ImageDraw, week_order: int):
    font = ImageFont.truetype(FONT_TYPE, WEEKBAR_FONT_SIZE)
    dow = 1
    x0 = MARGIN_LEFT
    y0 = WEEKBAR_Y
    for dow_order in range(1, 8):
        draw.text(
            (x0 + DOW_ANCHOR[0], y0 + DOW_ANCHOR[1]),
            get_dow_name(dow),
            font=font,
            fill=(0, 0, 0),
        )
        draw.text(
            (x0 + DATE_ANCHOR[0], y0 + DATE_ANCHOR[1]),
            get_date(week_order, dow_order),
            font=font,
            fill=(0, 0, 0),
        )
        x0 += COURSE_WIDTH
        dow = (dow + 1) % 7


# 获取要绘制的课表格子的坐标
def get_course_coordinate(
    dayOfWeek: int, startSection: int, endSection: int
) -> Tuple[int, int, int, int]:
    # 周日为 0 所以做 (dayOfWeek + 6) // 7 处理
    x0 = MARGIN_LEFT + COURSE_WIDTH * ((dayOfWeek + 6) % 7)
    y0 = COURSE_Y + COURSE_HEIGHT * (startSection - 1)
    x1 = x0 + COURSE_WIDTH
    y1 = y0 + (endSection - startSection + 1) * COURSE_HEIGHT
    # 课表格子间取间距
    x0 += COURSE_MARGIN
    y0 += COURSE_MARGIN
    x1 -= COURSE_MARGIN
    y1 -= COURSE_MARGIN
    return (x0, y0, x1, y1)


# 绘制某个课表格子 起始点 (x,y) 结束点 (x,y)
def draw_course(
    draw: ImageDraw.ImageDraw, xy: Tuple[int, int, int, int], course: Course
):
    font = ImageFont.truetype(FONT_TYPE, FONT_SIZE)
    draw.rounded_rectangle(
        xy=xy,
        radius=COURSE_RADIUS,
        outline=(255, 255, 255),
        fill=get_color(course.day_of_week),
        width=2,
    )
    draw.text(
        (xy[0] + COURSE_NAME_ANCHOR[0], xy[1] + COURSE_NAME_ANCHOR[1]),
        name_format(course.name, 4),
        font=font,
    )
    draw.text(
        (xy[0] + COURSE_ROOM_ANCHOR[0], xy[3] + COURSE_ROOM_ANCHOR[1]),
        place_format(course.room),
        font=font,
    )


def draw_courses(courses: List[Course], week_order: int, draw: ImageDraw.ImageDraw):
    for course in courses:
        if course.week_start > week_order or course.week_end < week_order:
            continue
        draw_course(
            draw,
            get_course_coordinate(
                course.day_of_week, course.section_start, course.section_end
            ),
            course,
        )


def draw_all(courses: List[Course], filename: str, week_order: int):
    width = BASE_WIDTH
    height = BASE_HEIGHT

    image = Image.new("RGBA", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw_topbar(draw, week_order)
    draw_weekbar(draw, week_order)
    draw_courses(courses, week_order, draw)
    image.save(
        "{}{}_{}.jpg".format(COURSE_PIC_SAVE_PATH, filename, str(week_order)), "png"
    )
