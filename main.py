from model.apires import BadRes, GoodRes
from fastapi import FastAPI
from pydantic import BaseModel
from jwc.picgen import *
from model.course import *
import requests
import json

app = FastAPI()


@app.get("/")
def test():
    return {"ok": True}


class JwcForm(BaseModel):
    username: str
    password: str


@app.post("/jwc/course/pic")
def get_course_pic(form: JwcForm):
    res = requests.post(
        "http://localhost:5901/api/jwc/json?username={}&password={}".format(
            form.username, form.password
        )
    )
    if not res.ok:
        return BadRes("下层服务错误")
    resJson = json.loads(res.text)
    if not resJson["ok"]:
        return BadRes("账号或密码错误")
    courses = ReadCourses(resJson["data"])
    draw_all(courses, "code", 3)
    return GoodRes("ok", None)
