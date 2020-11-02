from flask import Flask, render_template
from gpiozero import LEDBoard
#import Adafruit_DHT

app = Flask(__name__)

# leds의 핀번호 정의(BCM 핀번호)
leds = LEDBoard(14, 15, 18)

# leds의 상태 정보 저장을 위한 데이터
led_states = {
	'red':0,
	'green':0,
	'yellow':0
}

@app.route('/')
def hello():
    return 'Hello World!'


#@app.route('/temp')
#def temp_hum():
#    sensor = Adafruit_DHT.DHT11
#    pin = 17
#    humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
#    DHT = { 'temp' : temperature, 'humi' : humidity}
#    return render_template('index2.html',**DHT)


# ex) 192.168.1.57:5000/red/0
@app.route('/<color>/<int:state>')
def led_switch(color, state):
    led_states[color] = state
    leds.value=tuple(led_states.values())
    return render_template('index.html', led_states=led_states)

@app.route('/all/<int:state>')
def all_on_off(state):
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

    leds.value=tuple(led_states.values())
    return render_template('index.html', led_states=led_states)


if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5000, debug=True)

