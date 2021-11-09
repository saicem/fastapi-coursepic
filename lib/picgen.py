# 图片生成


from typing import List, Tuple
from model.course import Course
from PIL import Image, ImageDraw, ImageFont
from lib.config import *
from lib.util import *


class CourseDrawer:
    __image: Image
    __draw: ImageDraw.ImageDraw

    def __init__(self) -> None:
        self.__image = Image.new("RGBA", (BASE_WIDTH, BASE_HEIGHT), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__image)

    def draw_topbar(self, week_order: int):
        font = ImageFont.truetype(FONT_TYPE, TOPBAR_FONT_SIZE)
        self.__draw.text(
            WEEKORDER_ANCHOR,
            get_weekorder_name(week_order),
            font=font,
            fill=(12, 12, 12),
        )

    def draw_weekbar(self, week_order: int):
        font = ImageFont.truetype(FONT_TYPE, WEEKBAR_FONT_SIZE)
        dow = 1
        x0 = MARGIN_LEFT
        y0 = WEEKBAR_Y
        for dow_order in range(1, 8):
            self.__draw.text(
                (x0 + DOW_ANCHOR[0], y0 + DOW_ANCHOR[1]),
                get_dow_name(dow),
                font=font,
                fill=(0, 0, 0),
            )
            self.__draw.text(
                (x0 + DATE_ANCHOR[0], y0 + DATE_ANCHOR[1]),
                get_date(week_order, dow_order),
                font=font,
                fill=(0, 0, 0),
            )
            x0 += COURSE_WIDTH
            dow = (dow + 1) % 7

    # 获取要绘制的课表格子的坐标
    def get_course_coordinate(
        self, dayOfWeek: int, startSection: int, endSection: int
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
    def draw_course(self, course_box_xy: Tuple[int, int, int, int], course: Course):
        font = ImageFont.truetype(FONT_TYPE, FONT_SIZE)
        self.__draw.rounded_rectangle(
            xy=course_box_xy,
            radius=COURSE_RADIUS,
            outline=(255, 255, 255),
            fill=get_color(course.day_of_week),
            width=2,
        )
        self.draw_text_course_name(
            course.name,
            font,
            (course_box_xy[0] + COURSE_NAME_ANCHOR[0], course_box_xy[1] + COURSE_NAME_ANCHOR[1]),
        )
        self.draw_text_course_place(
            course.room,
            font,
            (course_box_xy[0] + COURSE_ROOM_ANCHOR[0], course_box_xy[3] + COURSE_ROOM_ANCHOR[1]),
        )

    def draw_courses(self, courses: List[Course], week_order: int):
        for course in courses:
            if course.week_start > week_order or course.week_end < week_order:
                continue
            self.draw_course(
                self.get_course_coordinate(
                    course.day_of_week, course.section_start, course.section_end
                ),
                course,
            )

    # 渲染课程名称
    def draw_text_course_name(
        self, text: str, font: ImageFont.FreeTypeFont, anchor
    ) -> None:
        draw_text = self.format_text(text, COURSE_TEXT_MAXLEN, font)
        self.__draw.text(
            (anchor[0], anchor[1]),
            draw_text,
            font=font,
        )

    # https://www.osgeo.cn/pillow/reference/ImageFont.html
    # 上课地点信息格式化
    def draw_text_course_place(
        self, text: str, font: ImageFont.FreeTypeFont, anchor
    ) -> None:
        draw_text = self.format_text(text, COURSE_TEXT_MAXLEN, font)
        # 对于固定的信息可以特别的处理
        # text.replace("(", "\n").replace(")", "")
        _, compensate_height = font.getsize_multiline(draw_text)
        self.__draw.text(
            (anchor[0], anchor[1] - compensate_height),
            draw_text,
            font=font,
        )

    def format_text(
        self, text: str, text_max_length: str, font: ImageFont.FreeTypeFont
    ):
        draw_text_list = []
        length = len(text)
        start: int = 0
        end: int = (8, length)[length > 5]
        while start < length:
            tmp_len = font.getlength(text[start:end])
            if tmp_len > text_max_length:
                end -= 1
            else:
                draw_text_list.append(text[start:end])
                start = end
                end = (end + 8, length)[length > end + 8]
        return "\n".join(draw_text_list)

    def draw_all(self, courses: List[Course], filename: str, week_order: int):
        if week_order <= 0 or week_order > 20:
            raise Exception(
                "week_order 应大于0小于等于20 而给予的 week_order = {}".format(week_order)
            )
        self.draw_topbar(week_order)
        self.draw_weekbar(week_order)
        self.draw_courses(courses, week_order)
        self.__image.save(
            "{}{}_{}.jpg".format(COURSE_PIC_SAVE_PATH, filename, str(week_order)), "png"
        )
