FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

EXPOSE 8000

COPY requirements.txt requirements.txt

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN mv ./src/fonts/HarmonyOS_Sans_SC_Regular.ttf /usr/share/fonts/HarmonyOS_Sans_SC_Regular.ttf && \
    mkdir ./cache/course_table

CMD [ "uvicorn" ,"main:app","--host", "0.0.0.0"]
