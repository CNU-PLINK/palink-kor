from pydantic import BaseModel
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    accountId: str
    name: str
    age: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None

class UserLogin(BaseModel):
    accountId: str
    password: str

class User(UserBase):
    userId: int

    class Config:
        from_attributes = True

class AiCharacterBase(BaseModel):
    aiName: str
    description: str
    difficultyLevel: int

class AiCharacterCreate(AiCharacterBase):
    pass

class AiCharacter(AiCharacterBase):
    characterId: int

    class Config:
        from_attributes = True

class AiCharacters(BaseModel):
    characters: List[AiCharacter]

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    day: datetime.datetime
    userId: int
    characterId: int

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    conversationId: int

    class Config:
        from_attributes = True

class Conversations(BaseModel):
    conversations: List[Conversation]

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    sender: bool
    messageText: str
    timestamp: datetime.datetime


class Message(MessageBase):
    messageId: int
    conversationId: int

    class Config:
        from_attributes = True

class Messages(BaseModel):
    messages: List[Message]

    class Config:
        from_attributes = True

# AIResponseBase: 기본 Pydantic 스키마
class AIResponseBase(BaseModel):
    text: str
    feeling: Optional[str] = None  # 필수 값이 아니므로 Optional로 설정
    affinity_score: int
    rejection_score: List[int]  # List of integer values
    rejection_content: List[str]  # List of string values
    final_rejection_score: int
    final_affinity_score: int

# AIResponseCreate: 데이터를 생성할 때 사용하는 스키마
class AIResponseCreate(AIResponseBase):
    feeling: Optional[str] = None  # 필수 값이 아니므로 Optional로 설정
    rejection_score: List[int]  # List of integer values
    rejection_content: List[str]  # List of string values
    final_rejection_score: Optional[int]  # Optional로 설정
    final_affinity_score: Optional[int]  # Optional로 설정

    class Config:
        orm_mode = True  # SQLAlchemy 모델과의 호환성 설정

# AIResponse: 데이터베이스 조회 시 사용하는 스키마
class AIResponse(AIResponseBase):
    aiMessage: int

    class Config:
        orm_mode = True

class MessageCreate(MessageBase):
    ai_response: Optional[AIResponseCreate] = None  # AI 응답은 선택 사항

class TipBase(BaseModel):
    messageId: int
    tipText: Optional[str] = None

class TipCreate(TipBase):
    pass

class Tip(TipBase):
    tipId: int

    class Config:
        from_attributes = True

class Tips(BaseModel):
    tips: List[Tip]

    class Config:
        from_attributes = True

class LikingBase(BaseModel):
    messageId: int
    likingLevel: Optional[int] = None
    characterId: int
    userId: int

class LikingCreate(LikingBase):
    pass

class Liking(LikingBase):
    likingId: int

    class Config:
        from_attributes = True

class Likings(BaseModel):
    likings: List[Liking]

    class Config:
        from_attributes = True

class MindsetBase(BaseModel):
    mindsetText: str

class MindsetCreate(MindsetBase):
    pass

class Mindset(MindsetBase):
    mindsetId: int

    class Config:
        from_attributes = True

class FeedbackBase(BaseModel):
    conversationId: int
    feedbackText: Optional[str] = None
    finalLikingLevel: Optional[int] = None
    totalRejectionScore: Optional[int] = None

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    feedbackId: int

    class Config:
        from_attributes = True

class Feedbacks(BaseModel):
    feedbacks: List[Feedback]

    class Config:
        from_attributes = True

class UserCollectionBase(BaseModel):
    characterId: int
    addedDate: datetime.datetime

class UserCollectionCreate(UserCollectionBase):
    pass

class UserCollection(UserCollectionBase):
    userId: int

    class Config:
        from_attributes = True

class UserCollections(BaseModel):
    userId: int
    characters: List[UserCollection]

    class Config:
        from_attributes = True

class EmotionBase(BaseModel):
    emotionType: str
    vibrationPattern: int
    backgroundColor: str
    messageId: int

class EmotionCreate(EmotionBase):
    pass

class Emotion(EmotionBase):
    emotionId: int

    class Config:
        from_attributes = True

class Emotions(BaseModel):
    emotions: List[Emotion]

    class Config:
        from_attributes = True

class RejectionBase(BaseModel):
    messageId: int
    rejectionLevel: Optional[int] = None
    characterId: int
    userId: int
    rejectionText: Optional[str] = None

class RejectionCreate(RejectionBase):
    pass

class Rejection(RejectionBase):
    rejectionId: int

    class Config:
        from_attributes = True

class Rejections(BaseModel):
    rejections: List[Rejection]

    class Config:
        from_attributes = True

