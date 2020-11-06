# models.py

# 외부 클래스 import
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func

# SQLAlchemy 객체를 하나 생성
db = SQLAlchemy()

# led 데이터 모델을 나타내는 객체를 하나 선언
# SQLAlchemy의 기능을 사용하기 위해 `db.Model`을 상속받기
class Myled(db.Model):
    __tablename__='led'	# led라는 데이터베이스 테이블 이름 지정
	
	# 테이블의 컬럼(속성, 필드)을 만들기 위해서는 `db.Column()`을 이용
    id = db.Column(db.Integer,primary_key=True)
    red = db.Column(db.Integer)
    green = db.Column(db.Integer)
    yellow = db.Column(db.Integer)
    #time = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    time = db.Column(db.String(30))