import json
from moviepy.editor import (
    VideoFileClip,
    VideoClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
)

def exporter(recognitions, video_filename, end_time):
    video = VideoFileClip(video_filename)

    fps = video.fps

    duration = video.duration

    total_frames = int(duration * fps)

    

    frame_duration = 1 / fps
    
    width = video.size[0]
    height = video.size[1]
    videoArea = width * height

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

            "detections": recog_formatter(recognitions, videoArea)
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
def recog_formatter(recognitions, videoArea):
    output = {}

    for recognition in recognitions:
        print(recognition)
        print("stop")
        boxes = recognition["boxes"]
        scores = recognition["scores"]
        brands = recognition["brands"]
        print(brands)
        area = []
        for box, in zip(boxes):
            #convert coordinates to int 
            x1, y1, x2, y2 = box

            length = abs(x1 -x2)
            width = abs(y1 - y2)
            
            area.append(length * width)

        score=mean(scores)
        areaPercentage = round(mean(area)/ videoArea, 2)

        
        
        output.append(
                {
                    "id": 1,
                    "type": "logo",
                    "name": brand,
                    "meta": {
                        "logoVersionId": 1
                        },
                    "iconUrl": "",
                    "size": size(areaPercentage),
                    "area": videoArea,
                    "areaPercentage": areaPercentage,
                    "timeBeing": "0:00:00.000",
                    "timeEnd": "0:00:00.000",
                    "confidence": score,
                    coordinates: {}
                }
            )


            
def size(areaPercentage):

    if areaPercentage < 0.01:
        return "tiny"
    elif areaPercentage < 0.1:
        return "small"
    else:
        return "large"


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

        