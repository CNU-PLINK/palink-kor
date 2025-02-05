from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import models, schemas
from database import engine, get_db, Base
from fastapi.middleware.cors import CORSMiddleware
from typing import List


app = FastAPI()

Base.metadata.create_all(bind=engine)
origins = [
    # "https://palink-v2.web.app",  # 웹앱 도메인
    "http://localhost"            # 로컬 테스트를 위한 설정
]
# CORS 설정
origins = ["*"]  # 모든 출처 허용

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.accountId == user.accountId).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Account ID already registered")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.User)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.accountId == user.accountId, models.User.password == user.password).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="ID 또는 비밀번호를 잘못 입력하였습니다.")
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.userId == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.patch("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.userId == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/conversations", response_model=schemas.Conversation)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = models.Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@app.get("/conversations/{conversation_id}", response_model=schemas.Conversation)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = db.query(models.Conversation).filter(models.Conversation.conversationId == conversation_id).first()
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@app.get("/conversations/users/{user_id}", response_model=schemas.Conversations)
def read_user_conversations(user_id: int, db: Session = Depends(get_db)):
    db_conversations = db.query(models.Conversation).filter(models.Conversation.userId == user_id).all()
    if not db_conversations:
        raise HTTPException(status_code=404, detail="해당 user id에 대한 대화를 찾을 수 없습니다.")
    return {"conversations": db_conversations}

@app.post("/conversations/{conversation_id}/messages", response_model=schemas.Message)
def create_message(conversation_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    # Create the message in the database
    db_message = models.Message(conversationId=conversation_id, sender=message.sender, messageText=message.messageText,
                                timestamp=message.timestamp)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # If the message is an AI response (sender=False)
    if not message.sender and message.ai_response:
        # Retrieve the user's last message
        previous_message = db.query(models.Message).filter(
            models.Message.conversationId == conversation_id,
            models.Message.messageId == db_message.messageId - 1
        ).first()

        if not previous_message:
            raise HTTPException(status_code=404, detail="Previous user message not found")

        # 해당 대화(conversation_id)에 해당하는 모든 AIResponse를 가져오기
        all_ai_responses = db.query(models.AIResponse).filter(
             models.AIResponse.conversation_id == conversation_id
        ).all()

        # 모든 rejection_score 리스트의 값을 합산
        total_rejection_score = sum(
            sum(ai_response.rejection_score) for ai_response in all_ai_responses
        )

        # 모든 affinity_score의 값을 합산
        total_affinity_score = sum(
            ai_response.affinity_score for ai_response in all_ai_responses
            if ai_response.affinity_score is not None
        )

        ai_response = models.AIResponse(
            aiMessage=db_message.messageId,
            text=db_message.messageText, #현재 ai가 보내는 답장 메시지
            feeling=message.ai_response.feeling,
            affinity_score=message.ai_response.affinity_score,
            rejection_score=message.ai_response.rejection_score,
            userMessage=previous_message.messageText, #이전에 유저가 보낸 말
            conversation_id=conversation_id,
            rejection_content=message.ai_response.rejection_content, #거절점수표에 있는 내용 (이유있는 거절 등)
            final_rejection_score=total_rejection_score + sum(message.ai_response.rejection_score), # 누적된 rejection_score
            final_affinity_score = total_affinity_score + message.ai_response.affinity_score  # 누적된 affinity_score
        )
        db.add(ai_response)
        db.commit()
        db.refresh(ai_response)

    return db_message

@app.get("/conversations/{conversation_id}/messages", response_model=schemas.Messages)
def read_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    db_messages = db.query(models.Message).filter(models.Message.conversationId == conversation_id).all()
    if not db_messages:
        raise HTTPException(status_code=404, detail="해당 conversation id에 대한 메시지를 찾을 수 없습니다.")
    return {"messages": db_messages}

@app.get("/conversations/{conversation_id}/messages/{message_id}", response_model=schemas.Message)
def read_message(conversation_id: int, message_id: int, db: Session = Depends(get_db)):
    db_message = db.query(models.Message).filter(models.Message.conversationId == conversation_id, models.Message.messageId == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.get("/conversations/{conversation_id}/airesponses")
def get_ai_responses_by_conversation(conversation_id: int, db: Session = Depends(get_db)):
    # 특정 conversationId에 해당하는 AIresponses 조회
    ai_responses = db.query(models.AIResponse).filter(models.AIResponse.conversation_id == conversation_id).all()

    if not ai_responses:
        raise HTTPException(status_code=404, detail=f"No AI responses found for conversation_id {conversation_id}")

    return ai_responses


@app.get("/conversations/{conversation_id}/messages/{message_id}/airesponses")
def get_ai_responses(conversation_id: int, message_id: int, db: Session = Depends(get_db)):
    # 특정 conversation_id와 message_id에 해당하는 AIresponses 조회
    ai_responses = db.query(models.AIResponse).filter(
        models.AIResponse.conversation_id == conversation_id,
        models.AIResponse.aiMessage == message_id
    ).all()

    if not ai_responses:
        raise HTTPException(status_code=404,
                            detail=f"No AI responses found for conversation_id {conversation_id} and message_id {message_id}")

    return ai_responses

@app.get("/conversations/{conversation_id}/airesponses", response_model=List[schemas.AIResponse])
def get_ai_responses_by_conversation(conversation_id: int, db: Session = Depends(get_db)):
    # Query AI responses by conversation_id
    ai_responses = db.query(models.AIResponse).filter(models.AIResponse.conversation_id == conversation_id).all()

    if not ai_responses:
        raise HTTPException(status_code=404, detail=f"No AI responses found for conversation_id {conversation_id}")

    return ai_responses


@app.get("/conversations/{conversation_id}/messages/{message_id}/airesponses", response_model=List[schemas.AIResponse])
def get_ai_responses_by_message(conversation_id: int, message_id: int, db: Session = Depends(get_db)):
    # Query AI responses by both conversation_id and message_id
    ai_responses = db.query(models.AIResponse).filter(
        models.AIResponse.conversation_id == conversation_id,
        models.AIResponse.aiMessage == message_id
    ).all()

    if not ai_responses:
        raise HTTPException(status_code=404,
                            detail=f"No AI responses found for conversation_id {conversation_id} and message_id {message_id}")

    return ai_responses

@app.post("/tips", response_model=schemas.Tip)
def create_tip(tip: schemas.TipCreate, db: Session = Depends(get_db)):
    db_tip = models.Tip(**tip.dict())
    db.add(db_tip)
    db.commit()
    db.refresh(db_tip)
    return db_tip

@app.get("/tips/{tip_id}", response_model=schemas.Tip)
def read_tip(tip_id: int, db: Session = Depends(get_db)):
    db_tip = db.query(models.Tip).filter(models.Tip.tipId == tip_id).first()
    if db_tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return db_tip

@app.get("/tips/messages/{message_id}", response_model=schemas.Tips)
def read_message_tips(message_id: int, db: Session = Depends(get_db)):
    db_tips = db.query(models.Tip).filter(models.Tip.messageId == message_id).all()
    if not db_tips:
        raise HTTPException(status_code=404, detail="해당 id에 대한 팁을 찾을 수 없습니다.")
    return {"tips": db_tips}

@app.get("/characters", response_model=schemas.AiCharacters)
def read_all_characters(db: Session = Depends(get_db)):
    db_characters = db.query(models.AiCharacter).all()
    return {"characters": db_characters}

@app.get("/characters/{character_id}", response_model=schemas.AiCharacter)
def read_character(character_id: int, db: Session = Depends(get_db)):
    db_character = db.query(models.AiCharacter).filter(models.AiCharacter.characterId == character_id).first()
    if db_character is None:
        raise HTTPException(status_code=404, detail="AiCharacter not found")
    return db_character

@app.post("/feedbacks", response_model=schemas.Feedback)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/conversations/{conversation_id}/feedbacks", response_model=schemas.Feedbacks)
def read_conversation_feedbacks(conversation_id: int, db: Session = Depends(get_db)):
    db_feedbacks = db.query(models.Feedback).filter(models.Feedback.conversationId == conversation_id).all()
    if not db_feedbacks:
        raise HTTPException(status_code=404, detail="해당 conversation id에 대한 피드백을 찾을 수 없습니다.")
    return {"feedbacks": db_feedbacks}

@app.post("/users/{user_id}/collections", response_model=schemas.UserCollection)
def create_user_collection(user_id: int, user_collection: schemas.UserCollectionCreate, db: Session = Depends(get_db)):
    db_user_collection = models.UserCollection(userId=user_id, **user_collection.dict())
    db.add(db_user_collection)
    db.commit()
    db.refresh(db_user_collection)
    return db_user_collection

@app.get("/users/{user_id}/collections", response_model=schemas.UserCollections)
def read_user_collections(user_id: int, db: Session = Depends(get_db)):
    db_user_collections = db.query(models.UserCollection).filter(models.UserCollection.userId == user_id).all()
    if not db_user_collections:
        raise HTTPException(status_code=404, detail="해당 user의 콜렉션을 찾을 수 없습니다.")
    return {"userId": user_id, "characters": db_user_collections}

@app.post("/emotions", response_model=schemas.Emotion)
def create_emotion(emotion: schemas.EmotionCreate, db: Session = Depends(get_db)):
    db_emotion = models.Emotion(**emotion.dict())
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

@app.get("/emotions/{emotion_id}", response_model=schemas.Emotion)
def read_emotion(emotion_id: int, db: Session = Depends(get_db)):
    db_emotion = db.query(models.Emotion).filter(models.Emotion.emotionId == emotion_id).first()
    if db_emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return db_emotion

@app.get("/emotions/messages/{message_id}", response_model=schemas.Emotions)
def read_message_emotions(message_id: int, db: Session = Depends(get_db)):
    db_emotions = db.query(models.Emotion).filter(models.Emotion.messageId == message_id).all()
    if not db_emotions:
        raise HTTPException(status_code=404, detail="해당 id에 대한 감정 데이터를 찾을 수 없습니다.")
    return {"emotions": db_emotions}

@app.get("/mindsets/random", response_model=schemas.Mindset)
def read_random_mindset(db: Session = Depends(get_db)):
    db_mindset = db.query(models.Mindset).order_by(func.random()).first()
    if db_mindset is None:
        raise HTTPException(status_code=404, detail="마인드셋을 찾을 수 없습니다.")
    return db_mindset

@app.get("/mindsets/{mindset_id}", response_model=schemas.Mindset)
def read_mindset(mindset_id: int, db: Session = Depends(get_db)):
    db_mindset = db.query(models.Mindset).filter(models.Mindset.mindsetId == mindset_id).first()
    if db_mindset is None:
        raise HTTPException(status_code=404, detail="Mindset not found")
    return db_mindset

@app.post("/likings", response_model=schemas.Liking)
def create_liking(liking: schemas.LikingCreate, db: Session = Depends(get_db)):
    db_liking = models.Liking(**liking.dict())
    db.add(db_liking)
    db.commit()
    db.refresh(db_liking)
    return db_liking

@app.get("/likings/{liking_id}", response_model=schemas.Liking)
def read_liking(liking_id: int, db: Session = Depends(get_db)):
    db_liking = db.query(models.Liking).filter(models.Liking.likingId == liking_id).first()
    if db_liking is None:
        raise HTTPException(status_code=404, detail="Liking not found")
    return db_liking

@app.get("/likings/messages/{message_id}", response_model=schemas.Likings)
def read_message_likings(message_id: int, db: Session = Depends(get_db)):
    db_likings = db.query(models.Liking).filter(models.Liking.messageId == message_id).all()
    if not db_likings:
        raise HTTPException(status_code=404, detail="해당 메시지 id에 대한 호감도를 찾을 수 없습니다.")
    return {"likings": db_likings}

@app.post("/rejections", response_model=schemas.Rejection)
def create_rejection(rejection: schemas.RejectionCreate, db: Session = Depends(get_db)):
    db_rejection = models.Rejection(**rejection.dict())
    db.add(db_rejection)
    db.commit()
    db.refresh(db_rejection)
    return db_rejection

@app.get("/rejections/conversations/{conversation_id}", response_model=schemas.Rejections)
def read_conversation_rejections(conversation_id: int, db: Session = Depends(get_db)):
    db_rejections = db.query(models.Rejection).filter(models.Rejection.conversationId == conversation_id).all()
    if not db_rejections:
        raise HTTPException(status_code=404, detail="해당 conversation id에 대한 거절 점수를 찾을 수 없습니다.")
    return {"rejections": db_rejections}

@app.get("/rejections/messages/{message_id}", response_model=schemas.Rejections)
def read_message_rejections(message_id: int, db: Session = Depends(get_db)):
    db_rejections = db.query(models.Rejection).filter(models.Rejection.messageId == message_id).all()
    if not db_rejections:
        raise HTTPException(status_code=404, detail="해당 메시지 id에 대한 거절 점수를 찾을 수 없습니다.")
    return {"rejections": db_rejections}
