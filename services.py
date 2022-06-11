#import aiofiles
import shutil
from uuid import uuid4

from fastapi import UploadFile, BackgroundTasks, HTTPException

from models import Video
from schemas import UploadVideo, User


async def save_video(
        file: UploadFile,
        user: User,
        background_tasks: BackgroundTasks,
        title: str,
        description: str
):
    file_name = f"media/{user.dict().get('id')}_{uuid4()}.mp4"
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't a mp4 flie")
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user, **info.dict())


def write_video(file_name: str, file: UploadFile):
    # async with aiofiles.open(file_name, 'wb') as buffer:
    #     data = await file.read()
    #     await buffer.write(data)
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
