import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
app = Flask(__name__)
model = pickle.load(open('model_final.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = [x for x in request.form.values()]
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=343c877db056b953447e1b48bb5f6421&q='
    city = features[0]
    url = api_address + city
    json_data = requests.get(url).json()
    format_add = json_data['base']
    float("{0:.2f}".format(json_data['main']['temp'] - 273.15))
    print("Max Temp={0:.1f}°C".format(int(json_data['main']['temp_max'] - 273.15)))
    TM = int(json_data['main']['temp_max'] - 273.15)
    Tm = int(json_data['main']['temp_min'] - 273.15)
    print("Min Temp={0:.1f}°C".format(int(json_data['main']['temp_min'] - 273.15 - 10)))
    print("Humidity={0:d}".format(json_data['main']['humidity']))
    H = int(json_data['main']['humidity'])
    print("Visibility={0:d} km".format(int(json_data['visibility'] / 1000)))
    VV = int(json_data['visibility'] / 1000)
    print("Wind={0:.1f} km\h".format(int((18 / 5) * json_data['wind']['speed'])))
    V = int((18 / 5) * json_data['wind']['speed'])
    output=[0]*7
    Tm-=5
    TM+=5
    for i in range(7):
        para = [0] * 9
        if i>=3:
            para[0] = TM+2
            para[1] = Tm+2
            para[2] = H-10
            para[3] = VV+1
            para[4] = V+5
        else:
            para[0] = TM
            para[1] = Tm
            para[2] = H
            para[3] = VV
            para[4] = V

        date = 5
        d = str(date) + '-' + str(5) + '-' + str(2021)
        import pandas as pd
        df = pd.Timestamp(d)
        nd = df.dayofweek
        para[6]=1
        print(para)

        final_features = [np.array(para)]
        prediction = model.predict(final_features)
        output[i] = prediction[0]+1
#
    level = 0
    mx = -1
    aq = {1: 'AQI Range 0-50 Concern: Good', 2: 'AQI Range 51-100 Concern: Moderate',
          3: 'AQI Range 101-150 Concern: Unhealthy for Sensitive Groups', 4: 'AQI Range 151-200 Concern: Unhealthy',
          5: 'AQI Range 201-300 Concern: Very Unhealthy', 1: 'AQI Range 301-500 Concern:Hazardous'}
    outputf=[]
    for i in range(7):
        outputf.append(aq[output[i]])
    print('-------Predicted Air Quality for {}------------'.format(city), output)
    l1='Weather Details of '+str(city)
    l2='Maximum Temperature:'+str(TM)+'°C'
    l3 = 'Minimum Temperature:' + str(Tm) + '°C'
    l4 = 'Humidity:' + str(H) + '%'
    l5 = 'Wind Speed:' + str(V) + 'km\h'
    l6 = 'Visibility:' + str(VV) + 'km'
    return render_template('index.html',l1=l1,l2=l2,l3=l3,l4=l4,l5=l5,l6=l6,p1='Day {}: Predicted Air Quality of {} is in {}'.format(1,city,outputf[0]),p2='Day {}: Predicted Air Quality of {} is in {}'.format(2,city,outputf[1]), p3='Day {}: Predicted Air Quality of {} is in {}'.format(3,city,outputf[2]), p4='Day {}: Predicted Air Quality of {} is in {}'.format(4,city,outputf[3]), p5='Day {}: Predicted Air Quality of {} is in {}'.format(5,city,outputf[4]), p6='Day {}: Predicted Air Quality of {} is in {}'.format(6,city,outputf[5]), p7='Day {}: Predicted Air Quality of {} is in {}'.format(7,city,outputf[6]))

if __name__ == "__main__":
    app.run(debug=True)