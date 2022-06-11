import shutil
from typing import List
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from models import Video, User
from schemas import UploadVideo, GetVideo, Message
from services import save_video

video_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@video_router.post('/')
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...)
):
    user = await User.objects.first()
    return await save_video(
        file=file,
        user=user,
        background_tasks=background_tasks,
        title=title,
        description=description
    )



@video_router.get('/video/{video_pk}', responses={404: {'model': Message}})
async def get_video(video_pk: int):
    # file = await Video.objects.select_related('user').get(pk=video_pk)
    # file_like = open(file.dict().get('file'), mode='rb')
    file_like = open('VID-20210618-WA0003.mp4', mode='rb')
    return StreamingResponse(file_like, media_type='video/mp4')


# async def fake_video_streamer():
#     for i in range(10):
#         yield b"some fake video bytes"
#
#
# @video_router.get("/fake")
# async def main():
#     return StreamingResponse(fake_video_streamer())
