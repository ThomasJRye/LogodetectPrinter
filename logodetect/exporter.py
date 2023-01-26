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

            "detections": recog_formatter(recognitions, videoArea, frame_duration)
            }


# formats recognitions into a json file
def recog_formatter(recognitions, videoArea, frame_duration):
    tinyOutput = {}
    smallOutput = {}
    largeOutput = {}

    
    for recognition in recognitions:
        brands_in_frame = []

        for box, score, brand in zip(recognition["boxes"], recognition["scores"], recognition["brands"]):
            tinyInFrame = {}
            smallInFrame = {}
            largeInFrame = {}

            # ignore logos already found in frame
            if not contains_dict_with_key(brands_in_frame, brand):

                # remember that brand has been found in frame
                brands_in_frame.append(brand)


                if size(box, videoArea) == "tiny":
                    # is exposure ongoing?
                    if contains_dict_with_key(tinyInFrame, brand):
                        tinyInFrame[brand] += frame_duration
                    else:
                        tinyInFrame[brand] = frame_duration
                elif size(box, videoArea) == "small":
                    if contains_dict_with_key(smallInFrame, brand):
                        smallInFrame[brand] += frame_duration
                    else:
                        smallInFrame[brand] = frame_duration
                else:
                    if contains_dict_with_key(largeInFrame, brand):
                        largeInFrame[brand] += frame_duration
                    else:
                        largeInFrame[brand] = frame_duration
            
            for brand in largeInFrame:
                delete_if_in_dict(smallInFrame, brand)
            for brand in smallInFrame:
                delete_if_in_dict(tinyInFrame, brand)

            add_dicts(tinyOutput, tinyInFrame)
            add_dicts(smallOutput, smallInFrame)
            add_dicts(largeOutput, largeInFrame)
        
        
        
            


    print(tinyOutput)
    print(smallOutput)
    print(largeOutput)

            

    print(recognition)
    print("stop")
    boxes = recognition["boxes"]
    scores = recognition["scores"]
    brands = recognition["brands"]
    print(brands)
    area = []

    i = 0
    output = {}
    for box, in zip(boxes):

        score=mean(scores)
        
        output[str(i)]  = {
                "id": 1,
                "type": "logo",
                "name": brands[0],
                "meta": {
                    "logoVersionId": 1
                    },
                "iconUrl": "",
                "size": size(box, videoArea),
                "area": videoArea,
                "areaPercentage": areaPercentage,
                "timeBeing": "0:00:00.000",
                "timeEnd": "0:00:00.000",
                "confidence": score,
                "coordinates": {}
            }
            
        i += 1

def areaPercentage(box, videoArea):
    x1, y1, x2, y2 = box

    length = abs(x1 -x2)
    width = abs(y1 - y2)
    
    area = length * width

    return round(area / videoArea, 2)
            
def size(box, videoArea):
    screenPercent = areaPercentage(box, videoArea)
    if screenPercent < 0.01:
        return "tiny"
    elif screenPercent < 0.1:
        return "small"
    else:
        return "large"


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def findExposures(recognition, ongoingExposures, frame_duration):
    output = []
    for box, score, brand in zip(recognition["boxes"], recognition["scores"], recognition["brands"]):
        for exposure in ongoingExposures:
            if brand == exposure[brand] and rectangle_similarity(box, exposure[box]) > 0.8:
                exposure["duration"] += frame_duration
            else:
                output.append(exposure)
                ongoingExposures.remove(exposure)
    
    return output



def rectangle_similarity(rect1, rect2):
    x1_1, y1_1, x2_1, y2_1 = rect1
    x1_2, y1_2, x2_2, y2_2 = rect2

    # Calculate the area of each rectangle
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    # Find the coordinates of the intersection rectangle
    x_overlap = max(0, min(x2_1, x2_2) - max(x1_1, x1_2))
    y_overlap = max(0, min(y2_1, y2_2) - max(y1_1, y1_2))
    intersection_area = x_overlap * y_overlap

    # Calculate the similarity as the ratio of the intersection area to the union area
    union_area = area1 + area2 - intersection_area
    similarity = intersection_area / union_area

    return similarity

def contains_dict_with_key(arr, key):
    return any(key in d for d in arr)

def add_dicts(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]

def delete_if_in_dict(dict, key):
    if key in dict:
        del dict[key]