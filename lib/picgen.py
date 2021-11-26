# 图片生成


from typing import List, Tuple
from model.model import Course
from PIL import Image, ImageDraw, ImageFont
from lib.config import *
from lib.util import *


class CourseDrawer:
    __image: Image
    __draw: ImageDraw.ImageDraw
    __weekorder: int
    __courses: List[Course]

    def __init__(self, courses: List[Course], weekorder: int) -> None:
        self.__image = Image.new("RGBA", (BASE_WIDTH, BASE_HEIGHT), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__image)
        self.__weekorder = weekorder
        self.__courses = courses

    def draw_topbar(self):
        font = ImageFont.truetype(FONT_TYPE, TOPBAR_FONT_SIZE)
        self.__draw.text(
            WEEKORDER_ANCHOR,
            get_weekorder_name(self.__weekorder),
            font=font,
            fill=(12, 12, 12),
        )

    def draw_weekbar(self):
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
                get_date(self.__weekorder, dow_order),
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
            fill=get_color(course.DayOfWeek),
            width=2,
        )
        self.draw_text_course_name(
            course.Name,
            font,
            (
                course_box_xy[0] + COURSE_NAME_ANCHOR[0],
                course_box_xy[1] + COURSE_NAME_ANCHOR[1],
            ),
        )
        self.draw_text_course_place(
            course.Room,
            font,
            (
                course_box_xy[0] + COURSE_ROOM_ANCHOR[0],
                course_box_xy[3] + COURSE_ROOM_ANCHOR[1],
            ),
        )

    def draw_courses(self):
        for course in self.__courses:
            if course.WeekStart > self.__weekorder or course.WeekEnd < self.__weekorder:
                continue
            self.draw_course(
                self.get_course_coordinate(
                    course.DayOfWeek, course.WeekStart, course.WeekEnd
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
        text = self.format_text(text, COURSE_TEXT_MAXLEN, font)
        _, compensate_height = font.getsize_multiline(text)
        self.__draw.text(
            (anchor[0], anchor[1] - compensate_height),
            text,
            font=font,
        )

    def format_text(self, text: str, maxlen: int, font: ImageFont.FreeTypeFont) -> str:
        length = len(text)
        if len(text) <= 1:
            return text
        texts = []
        left: int = 0
        right: int = 1
        while 1:
            if right == length:
                texts.append(text[left:right])
                break
            if font.getlength(text[left : right + 1]) > maxlen:
                texts.append(text[left:right])
                left = right
            right += 1
        return "\n".join(texts)

    def draw(self, filename: str):
        self.draw_topbar()
        self.draw_weekbar()
        self.draw_courses()
        self.__image.save(f"{COURSE_PIC_SAVE_PATH}{filename}.jpg", "png")
