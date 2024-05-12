from fastapi import FastAPI, Depends, HTTPException
from models import Base, User
from schemas import UserSchema
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import json
from script import verifyFace
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a specific list of allowed origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return {"message": "Hello, World!"}

@app.post("/updateuser")
async def add_or_create_user(request:UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        user = User(username=request.username, faces=json.dumps(request.faces))
        db.add(user)
        
    else:
        faces = json.loads(user.faces) or []
        faces.append(request.faces[0])
        user.faces = json.dumps(faces)
    db.commit()
    db.refresh(user)
    return user

@app.post("/verifyUser")
async def verify_user(request:UserSchema, db: Session = Depends(get_db)):
    print("username", request.username)
    user = db.query(User).filter(User.username == request.username).first()
    print("user", user)
    if not user:
       raise HTTPException(status_code=404, detail="User not found!")
    else:
        faces = json.loads(user.faces)
        return verifyFace(faces, request.faces[0])

@app.get("/user/{user_name}")
async def get_users(user_name,db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username == user_name).first()
    return users