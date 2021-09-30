from fastapi import responses
from model.apires import BadRes, GoodRes
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from jwc.picgen import *
from model.course import *
from config import *
from jwc.config import *
import requests
import json
from tool import create_randstr, cache

app = FastAPI()


@app.get("/")
def test():
    return {"ok": True}


class CoursePicForm(BaseModel):
    username: str
    password: str
    week_order: int


@app.post("/jwc/course/pic")
def get_course_pic(form: CoursePicForm):
    res = requests.post(
        "{}/api/jwc/json?username={}&password={}&weekOrder={}".format(
            URL_JWC, form.username, form.password, form.week_order
        )
    )
    if not res.ok:
        return BadRes("下层服务错误")
    resJson = json.loads(res.text)
    if not resJson["ok"]:
        return BadRes("账号或密码错误")
    if resJson["data"] == None:
        return BadRes("没有课程信息")
    courses = ReadCourses(resJson["data"])
    draw_all(courses, form.username, form.week_order)

    token = create_randstr(32)
    cache.add(token, form.username)
    return GoodRes("ok", "/jwc/course/pic/{}".format(token))


@app.get("/jwc/course/pic/{token}")
async def create_file(token: str):
    value = cache.get(token)
    if value == None:
        raise HTTPException(status_code=406, detail="wrong token")
    return FileResponse(
        "{}{}.jpg".format(COURSE_PIC_SAVE_PATH, value), filename="course.jpg"
    )
