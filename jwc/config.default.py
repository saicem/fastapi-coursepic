import datetime

HOSTNAME = "localhost"

# 150 * 7 + 30
# 字体
FONT_TYPE = "simfang.ttf"
FONT_SIZE = 31
# 页边
MARGIN_TOP = 10
MARGIN_RIGHT = 10
MARGIN_BUTTOM = 40
MARGIN_LEFT = 10
# 每单元的长度 根据是两节课还是三节课而变化
COURSEBOX_HEIGHT = 170
COURSEBOX_WIDTH = 150
COURSE_MARGIN = 3
COURSE_RADIUS = 10
COURSE_NAME_BASE = (10, 10)
COURSE_ROOM_BASE = (10, -110)
# topbar
TOPBAR_HEIGHT = 40
TOPBAR_FONT_SIZE = 20
DOW_BASE = (52, 8)
DATE_BASE = (53, 28)
# lineCharNum = 10
# lineNum = 3
# time
DAY_BASE = datetime.datetime.strptime("2021-09-05", "%Y-%m-%d")
WEEK_SPAN = datetime.timedelta(days=7)
DAY_SPAN = datetime.timedelta(days=1)
COURSE_PIC_SAVE_PATH = "./src/jpg/"
