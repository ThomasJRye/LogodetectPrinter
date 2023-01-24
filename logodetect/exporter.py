import json
from moviepy.editor import (
    VideoFileClip,
    VideoClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
)

def exporter(recognitions, video_filename, end_time):
    recog_formatter(recognitions)
    video = VideoFileClip(video_filename)

    fps = video.fps

    duration = video.duration

    total_frames = int(duration * fps)

    width = video.size[0]

    height = video.size[1]

    frame_duration = 1 / fps
    


    data = {
        "dataRootName": "data", 
        "data": {
            "status": 200, 
            "mediaInfo": {
                "frames": total_frames, "width": width, "fps": fps, "height": height
                },
            "processTime": {
                "time": end_time, "unit": "seconds"
                }
            }, 
            "renderedediaUrl": "",
            "csvUrl": "",

            "recognitions": recognitions
            }

    #print(data)
    # print("recognitions: " )

    # print(recognitions)

    # print("filename: " )

    # print(video_filename)

    # print("frame_duration: " )

    # print(frame_duration)

    # print("total_frames: " )

    # print(total_frames)

# formats recognitions into a json file
def recog_formatter(recognitions):
    output = {}

    boxes = recognitions[0]['boxes'][0]

    for recognition in recognitions:
        boxes = recognition["boxes"]
        scores = recognition["scores"]
        brands = recognition["brands"]

        for box, score, brand in zip(boxes, scores, brands):
            #convert coordinates to int 
            box = [int(b) for b in box]

            x1, y1, x2, y2 = box

            length = abs(x1 -x2)
            width = abs(y1 - y2)
            area = length * width
            print(area)





    print(boxes)


    print("recognitions")
    print(recognitions)

        