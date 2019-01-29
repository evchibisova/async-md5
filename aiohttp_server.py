from aiohttp import web, ClientSession
from uuid import uuid4
from aiojobs.aiohttp import setup, spawn
from hashlib import md5
import smtplib


async def submit_handler(request):
    """
    берем email из POST
    добавляем в словарь tasks uuid файла и статус running
    возвращаем пользователю uuid
    """
    data = await web.Request.post(request)
    email, url = data["email"], data["url"]
    task_id = str(uuid4())
    tasks[task_id] = {"md5": None, "status": "running", "url": url}
    await spawn(request, perform_task(task_id, url, email))
    return web.Response(text=str({"id": task_id}) + "\n")


async def perform_task(task_id, url, email):
    file_md5 = await get_md5_hash(url)
    tasks[task_id]["md5"] = file_md5
    tasks[task_id]["status"] = "done"
    if email:
        send_email(email, "file URL: {}\nMD5: {}".format(url, file_md5))


async def get_md5_hash(url):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            h = md5()
            while True:
                data = await resp.content.read(1024)
                if not data:
                    break
                h.update(data)
            return h.hexdigest()


def send_email(email, msg):
    with open("email_data.txt", "r") as f:
        your_email, your_password, smtp_serv, smtp_port = f.read().split("\n")[:4]
    server = smtplib.SMTP_SSL(smtp_serv, smtp_port)
    server.login(your_email, your_password)
    server.sendmail(your_email, email, msg)
    server.quit()


async def check_handler(request):
    """
    take id from GET
    return result data from results dictionary (depends on status)
    """
    id = request.rel_url.query["id"]
    if id not in tasks:
        text = "task does not exist"
    elif tasks[id]["status"] == "done":
        text = str(tasks[id])
    else:
        text = "status: {}".format(tasks[id]["status"])
    return web.Response(text=text + "\n")


tasks = dict()
app = web.Application()
setup(app)
app.add_routes([web.get("/check", check_handler),
                web.post("/submit", submit_handler)])
web.run_app(app, host="127.0.0.1", port=8000)

