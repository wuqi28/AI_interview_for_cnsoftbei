import os
import librosa
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoConfig, Wav2Vec2FeatureExtractor, HubertPreTrainedModel, HubertModel

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

MODEL_NAME = "xmj2002/hubert-base-ch-speech-emotion-recognition"
SAMPLE_RATE = 16000
DURATION = 6


def id2class(idx: int) -> str:
    labels = ["angry", "fear", "happy", "neutral", "sad", "surprise"]
    return labels[idx] if 0 <= idx < len(labels) else "unknown"


class HubertClassificationHead(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.classifier_dropout)
        self.out_proj = nn.Linear(config.hidden_size, config.num_class)

    def forward(self, x):
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)
        return x


class HubertForSpeechClassification(HubertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.hubert = HubertModel(config)
        self.classifier = HubertClassificationHead(config)
        self.init_weights()

    def forward(self, x):
        outputs = self.hubert(x)
        hidden_states = outputs[0]
        x = torch.mean(hidden_states, dim=1)
        x = self.classifier(x)
        return x


def load_model():
    config = AutoConfig.from_pretrained(MODEL_NAME)
    processor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
    model = HubertForSpeechClassification.from_pretrained(MODEL_NAME, config=config)
    model.eval()
    return processor, model


def predict_emotion(audio_path: str, processor, model) -> dict:
    """对输入音频进行情绪预测，返回字典结果"""
    speech, sr = librosa.load(path=audio_path, sr=SAMPLE_RATE)
    inputs = processor(
        speech,
        padding="max_length",
        truncation=True,
        max_length=DURATION * SAMPLE_RATE,
        return_tensors="pt",
        sampling_rate=sr
    ).input_values

    with torch.no_grad():
        logits = model(inputs)
        scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
        pred_id = torch.argmax(logits).item()
        pred_label = id2class(pred_id)
        confidence = float(scores[pred_id])

    return {
        "path": audio_path,
        "label": pred_label,
        "confidence": confidence,
        "all_scores": scores.tolist()
    }


# ✅ 测试示例（可注释）
if __name__ == "__main__":
    processor, model = load_model()
    result = predict_emotion("./CASIA/6/sad/201-sad-zhaoquanyin.wav", processor, model)
    print(result)
