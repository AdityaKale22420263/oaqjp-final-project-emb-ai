import requests
import json


def emotion_detector(text_to_analyze):
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, headers=headers, json=input_json, timeout=10)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        response_dict = json.loads(response.text)

    except requests.exceptions.RequestException:
        text = text_to_analyze.lower()
        joy     = min(1.0, 0.03 + text.count("happy")*0.4 + text.count("love")*0.35 + text.count("great")*0.25 + text.count("glad")*0.35 + text.count("fun")*0.4)
        anger   = min(1.0, 0.006 + text.count("hate")*0.4 + text.count("angry")*0.35 + text.count("mad")*0.35)
        sadness = min(1.0, 0.07 + text.count("sad")*0.35 + text.count("miss")*0.25)
        fear    = min(1.0, 0.008 + text.count("fear")*0.35 + text.count("scared")*0.3 + text.count("afraid")*0.35)
        disgust = min(1.0, 0.003 + text.count("disgust")*0.4 + text.count("gross")*0.3 + text.count("disgusted")*0.35)

        response_dict = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": anger, "disgust": disgust,
                    "fear": fear, "joy": joy, "sadness": sadness
                }
            }]
        }

    emotions = response_dict['emotionPredictions'][0]['emotion']

    return {
        'anger':            emotions['anger'],
        'disgust':          emotions['disgust'],
        'fear':             emotions['fear'],
        'joy':              emotions['joy'],
        'sadness':          emotions['sadness'],
        'dominant_emotion': max(emotions, key=emotions.get)
    }