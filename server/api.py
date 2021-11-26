from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from lib.picgen import *
from model.model import CourseForm
from tool import randstr, cache
import hashlib
import json

app = FastAPI()


@app.get("/")
def test():
    return {"ok": True}


@app.post("/course/pic")
def get_course_pic(form: CourseForm):
    if form.WeekOrder < 0 or form.WeekOrder > 20:
        raise HTTPException(
            status_code=400,
            detail=f"week_order 应大于0小于等于20 而给予的 week_order = {form.WeekOrder}",
        )

    # digest = hashlib.sha224(bytes()).hexdigest()
    digest = "asd"

    flag = cache.get(digest)
    # TODO 格式化返回值
    if flag != None:
        return f"/jwc/course/pic/{digest}.jpg"

    # TODO 从文件列表查找摘要以避免再次生成
    # TODO 参数为0时渲染所有课表
    CourseDrawer(form.Courses, form.WeekOrder).draw(digest)
    flag = randstr(32)
    cache.add(digest, flag)
    cache.add(flag, digest)
    return f"/jwc/course/pic/{digest}.jpg"


@app.get("/course/pic/{flag}")
async def create_file(flag: str):
    digest = cache.get(flag)
    if digest == None:
        raise HTTPException(status_code=400, detail="链接已失效")
    return FileResponse(f"{COURSE_PIC_SAVE_PATH}{digest}.jpg", filename="course.jpg")
