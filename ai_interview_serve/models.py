from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    interviews = db.relationship("InterviewRecordModel", backref="user", lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'join_time': self.join_time.strftime("%Y-%m-%d %H:%M:%S"),
        }


class InterviewRecordModel(db.Model):
    __tablename__ = "interview_record"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    interviewer_name = db.Column(db.String(100), nullable=False)
    interview_style = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    spend_time = db.Column(db.Integer, default=0)
    current_interview_id = db.Column(db.String(100), nullable=False)

    turns = db.relationship("InterviewTurnModel", backref="interview", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "interviewer_name": self.interviewer_name,
            "interview_style": self.interview_style,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "spend_time": self.spend_time,
            "current_interview_id": self.current_interview_id,
        }


class InterviewTurnModel(db.Model):
    __tablename__ = "interview_turn"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interview_record.id"), nullable=False)
    round = db.Column(db.Integer)  # 回答轮数
    ai_time = db.Column(db.String(10), nullable=False)  # AI发言时间
    speaker_time = db.Column(db.String(10), nullable=False)  # 面试者发言时间
    audio_path = db.Column(db.String(200), nullable=False)  # 音频地址
    ai_interviewer_text = db.Column(db.Text)  # AI发言
    speaker_text = db.Column(db.Text)  # 面试者发言
    advanced_text = db.Column(db.Text)  # 改进的对话

    # 视频分析
    face_emotion = db.Column(db.Boolean)  # 面部情绪分析 true:放松 | false:紧张
    is_focused = db.Column(db.Boolean)  # 是否专注屏幕
    average_bearing_degrees = db.Column(db.Float)  # 视线角度
    average_gaze_strength = db.Column(db.Float)  # 平均视线强度，小于0.10就是专注于屏幕

    # 音频分析字段
    voice_emotion = db.Column(db.String(50))  # 音频情绪
    audio_avg_pitch = db.Column(db.Float)  # 平均音高（Hz）
    audio_speech_time = db.Column(db.Float)  # 有效语音时长（秒）
    audio_pause_time = db.Column(db.Float)  # 静音时长（秒）
    audio_pause_ratio = db.Column(db.Float)  # 静音占比（0~1之间）
    audio_pause_count = db.Column(db.Integer)  # 停顿次数
    audio_words_per_minute = db.Column(db.Float)  # 语速（词/分钟）

    def to_dict(self):
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "round": self.round,
            "ai_time": self.ai_time,
            "speaker_time": self.speaker_time,
            "audio_path": self.audio_path,
            "voice_emotion": self.voice_emotion,
            "face_emotion": self.face_emotion,
            "is_focused": self.is_focused,
            "ai_interviewer_text": self.ai_interviewer_text,
            "speaker_text": self.speaker_text,
            "advanced_text": self.advanced_text,
            "audio_avg_pitch": self.audio_avg_pitch,
            "audio_speech_time": self.audio_speech_time,
            "audio_pause_time": self.audio_pause_time,
            "audio_pause_ratio": self.audio_pause_ratio,
            "audio_pause_count": self.audio_pause_count,
            "audio_words_per_minute": self.audio_words_per_minute
        }
