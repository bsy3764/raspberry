# led app.py

import os
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from gpiozero import LEDBoard
from models import db
#import Adafruit_DHT

# import 추가한 내용
import datetime	# 시간 출력을 위해
from models import Myled	# db models.py
import time

app = Flask(__name__)	# 실행하는 ip, port 주소???

# leds의 핀번호 정의(BCM 핀번호)
leds = LEDBoard(14, 15, 18)
#print(type(leds))	# <class 'gpiozero.boards.LEDBoard'>


# leds의 상태 정보 저장을 위한 데이터
led_states = {
	'red':0,
	'green':0,
	'yellow':0
}
#print(type(led_states))	# <class 'dict'>

# 0.0.0.0:5000/
@app.route('/')
def hello():
    return 'Hello World!'
    
# ex) 0.0.0.0:5000/red/0
@app.route('/<color>/<int:state>', methods=['GET', 'POST'])
def led_switch(color, state):
    if request.method == 'GET':
        # 현재 시간을 저장, 위의 import datetime 이 필요
        now = datetime.datetime.now()
        led_time = now.strftime('%Y-%m-%d %H:%M:%S')
        #print(led_time)

        # led_states 전역변수 선언
        global led_states
     
        led_states[color] = state	# 해당 color를 키 값으로 state란 value를 수정
        leds.value=tuple(led_states.values())	# dict의 value만 뽑아 dict_values란 객체를 튜플로 만들기
        
        
        # led변수에 `Myled` 데이터 모델에 대한 인스턴스를 만들어 저장(led테이블??)
        led = Myled()
        
        # id는 models.py에서 primary_key=True 로 설정하였으므로 자동을 증가됨
        # id = request.form.get('id')
        
        # request.form.get는 post방식으로 보낼 때 사용하므로 get으론 다른 방식이 필요
        # red = request.form.get('red')
        # green = request.form.get('green')
        # yellow = request.form.get('yellow')
        # time = request.form.get('led_time') 

        # 기존의 state의 상태 저장하기
        # 0.0.0.0:5000/red/1 하고 0.0.0.0:5000/green/1 을 하면
        # red / green / yellow 가 1 / 1 / 0 처럼 유지하기 위해서;;;;
        red, green, yellow = leds.value        
        
        # db에 저장하기
        led.red = red
        led.green = green
        led.yellow = yellow
        led.time = led_time
        
        print("red:{},green:{},yellow:{}".format(red,green,yellow))
        
        # 데이터 베이스에 insert
        db.session.add(led)
        # 변경 내용을 저장
        db.session.commit()


    return render_template('index.html', led_states=led_states, led_time=led_time)

# 0.0.0.0:5000/all/1
@app.route('/all/<int:state>', methods=['GET', 'POST'])
def all_on_off(state):
    if request.method == 'GET':
        # led_states 전역변수 선언
        global led_states 
        # 현재 시간을 저장, 위의 import time 이 필요
        now = datetime.datetime.now()
        led_time = now.strftime('%Y-%m-%d %H:%M:%S')

        if state is 0:
            led_states={
                'red':0,
                'green':0,
                'yellow':0
            }
        elif state is 1:
            led_states={
                'red':1,
                'green':1,
                'yellow':1
            }
            
        # led변수에 `Myled` 데이터 모델에 대한 인스턴스(객체)를 만들어 저장(led테이블??)
        led = Myled()
        
        leds.value=tuple(led_states.values())
        
        red, green, yellow = leds.value        
        
        print("red:{},green:{},yellow:{}".format(red,green,yellow))
        
        # db에 저장하기
        led.red = red
        led.green = green
        led.yellow = yellow
        led.time = led_time
        
        # 데이터 베이스에 insert
        db.session.add(led)
        # 변경 내용을 저장
        db.session.commit()
        
    return render_template('index.html', led_states=led_states, led_time=led_time)


if __name__ == "__main__":    # 직접 해당 파일을 실행 시, app이 실행됨
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)
    print(__name__)

    dbfile = os.path.join(basedir, "db.sqlite")

	# sqlite db 접속 주소
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
	# 각 리쿼스트의 끝에 db 변동 사항을 자동 commit함
    app.config['SQLALCHEMY_COMMIT_IN_TEARDOWN'] = True
	# 개체 수정을 추적????? -> sqlAlchemy의 이벤트 기능을 사용할지에 대한 flag( 버그가 많데요 이 기능에 )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db
    # 초기화
    db.init_app(app)    # models.py에서 db = SQLAlchemy()가 있어서 가능함
    db.app=app
    db.create_all() # 테이블을 생성
    app.run(host='0.0.0.0', port=5000, debug=True)

