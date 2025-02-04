from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from database import Base
import enum

class User(Base):
    __tablename__ = "user"
    userId = Column(Integer, primary_key=True, index=True)
    accountId = Column(String(50), unique=True, index=True)
    name = Column(String(50))
    password = Column(String(100))
    age = Column(Integer)

class AiCharacter(Base):
    __tablename__ = "aicharacter"
    characterId = Column(Integer, primary_key=True, index=True)
    aiName = Column(String(50))
    description = Column(Text)
    difficultyLevel = Column(Integer)

class Conversation(Base):
    __tablename__ = "conversation"
    conversationId = Column(Integer, primary_key=True, index=True)
    day = Column(DateTime)
    userId = Column(Integer, ForeignKey("user.userId"))
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"))

    # Message와의 1:N 관계 (하나의 대화창에 여러 개의 메시지가 포함)
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "message"
    messageId = Column(Integer, primary_key=True, index=True)
    conversationId = Column(Integer, ForeignKey("conversation.conversationId"), nullable=False)
    sender = Column(Boolean, nullable=False)
    messageText = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # Conversation과의 N:1 관계 (하나의 메시지는 하나의 대화에 속함)
    conversation = relationship("Conversation", back_populates="messages")

    # AIResponse와의 1:1 관계, foreign_keys 명시
    ai_response = relationship("AIResponse", back_populates="message", uselist=False,
                               foreign_keys="[AIResponse.aiMessage]")

class AIResponse(Base):
    __tablename__ = "AIResponses"

    aiMessage = Column(Integer, ForeignKey("message.messageId"), primary_key=True, index=True)
    text = Column(Text, nullable=False)
    feeling = Column(Text)
    affinity_score = Column(Integer)
    rejection_score = Column(JSON)  # JSON 형태로 리스트 값 저장 가능
    rejection_content = Column(JSON)
    userMessage = Column(Text)
    final_rejection_score = Column(Integer)
    final_affinity_score = Column(Integer)
    conversation_id = Column(Integer, ForeignKey("message.conversationId"))

    # Message와의 1:1 관계, 외래 키 명시
    message = relationship("Message", back_populates="ai_response", foreign_keys=[aiMessage])

class Tip(Base):
    __tablename__ = "tip"
    tipId = Column(Integer, primary_key=True, index=True)
    messageId = Column(Integer, ForeignKey("message.messageId"))
    tipText = Column(Text)

class Liking(Base):
    __tablename__ = "liking"
    likingId = Column(Integer, primary_key=True, index=True)
    messageId = Column(Integer, ForeignKey("message.messageId"))
    likingLevel = Column(Integer)
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"))
    userId = Column(Integer, ForeignKey("user.userId"))

class Mindset(Base):
    __tablename__ = "mindset"
    mindsetId = Column(Integer, primary_key=True, index=True)
    mindsetText = Column(Text)

class Feedback(Base):
    __tablename__ = "feedback"
    feedbackId = Column(Integer, primary_key=True, index=True)
    conversationId = Column(Integer, ForeignKey("conversation.conversationId"))
    feedbackText = Column(Text)
    finalLikingLevel = Column(Integer)
    totalRejectionScore = Column(Integer)

class Rejection(Base):
    __tablename__ = "rejection"
    rejectionId = Column(Integer, primary_key=True, index=True)
    messageId = Column(Integer, ForeignKey("message.messageId"))
    rejectionLevel = Column(Integer)
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"))
    userId = Column(Integer, ForeignKey("user.userId"))
    rejectionText = Column(Text)

class UserCollection(Base):
    __tablename__ = "usercollection"
    userId = Column(Integer, ForeignKey("user.userId"), primary_key=True)
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"), primary_key=True)
    addedDate = Column(DateTime)

class Emotion(Base):
    __tablename__ = "emotion"
    emotionId = Column(Integer, primary_key=True, index=True)
    emotionType = Column(String(50))
    vibrationPattern = Column(Integer)
    backgroundColor = Column(String(20))
    messageId = Column(Integer, ForeignKey("message.messageId"))
