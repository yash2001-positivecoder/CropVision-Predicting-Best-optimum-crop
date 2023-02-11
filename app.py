from flask import Flask,request,url_for,redirect,render_template
import pickle
import numpy as np
import openai
import pandas as pd
data=pd.read_csv("rainfall.csv")

openai.api_key = "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"
model_engine = "text-davinci-003"
city=""
month=""
state=""
soil=""
nitrogen=0
phosphorous=0
potassium=0
rainfall =0
humidity = 0
temp = 0
ph = 0
season=0
flag=True
ph_list={"Alluvial soil":7.75,"Red soil":7.3,"Black soil":7.85,"Arid soil":8.0,"Laterite soil":6.5,"Saline soil":7.1,"Marshy soil":5.5,"Forest soil":6.2,"Sub-mountain soil":4.1}

rabi_list=["november","december","january","february","march","april","may"]
kharif_list=["june","july","august","september","october"]
basicmodel=pickle.load(open('basic_model.pkl','rb'))
advancemodel=pickle.load(open('advance_model.pkl','rb'))
input=[]
crops={1:"Rice",2:"Maize",3:"ChickPea",4:"Kidneybeans",5:"pigeonpeas",6:"Mothbeans",7:"Mungbeans",8:"Blackgram",9:"Lentil",10:"Pomegranate",11:"Banana",12:"Mango",13:"Grapes",14:"Watermelon",15:"Muskmelon",16:"Apple",17:"Orange",18:"Papaya",19:"Coconut",20:"Cotton",21:"Jute",22:"Coffee"}
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    features1=[x for x in request.form.values()]
    final=[np.array(features1)]
    return render_template("header.html")

@app.route('/survey.html',methods=['POST','GET'])

def survey():
    global city,month,state,soil,rainfall,humidity,temp,ph,flag,nitrogen,phosphorous,potassium,input,season
    if(request.method=="POST"):
        features2=[x for x in request.form.values()]
        final1=[np.array(features2)]
        # print(final1)
    #     city=final[0]
    #     state=final[1]
    #     month=final[2]
    #     soil=final[3]
    #     if(month.lower() in rabi_list):
    #         season=1
    #     elif(month.lower() in kharif_list):
    #         season=0
    #     else:
    #         season=10        
    #     if(final[4]=="Yes" or final[4]=="yes" ):
    #         nitrogen=final[5]
    #         phosphorous=final[6]
    #         potassium=final[7]
    #         flag=True
    #     else:
    #         flag=False    

    #     completion1 = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=prompt_rainfall,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    #     )
    #     completion2 = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=prompt_humidity,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    #     )

    #     completion3 = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=prompt_temp,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    #     )
    #     completion4 = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=prompt_ph,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    #     )
    #     rainfall = int(completion1.choices[0].text)
    #     humidity = int(completion2.choices[0].text)
    #     temp = int(completion3.choices[0].text)
    #     ph = int(completion4.choices[0].text)
    # # print(features)
    # # print(final)
    return render_template("survey.html")

ans=""
@app.route('/predict.html',methods=['POST','GET'])
def predict():
    global city,month,state,soil,rainfall,humidity,temp,ph,flag,nitrogen,phosphorous,potassium,input,season,prompt_temp,prompt_ph,prompt_humidity,prompt_rainfall
    
    if(request.method=="POST"):
        features=[x for x in request.form.values()]
        final1=[np.array(features)]
        city=features[0]
        state=features[1]
        month=features[2]
        soil=features[3]
        # prompt_rainfall = "What is avg rainfall in the month of %s in %s District in state %s. Do not give any textual ans and Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(month,city,state)
        prompt_humidity="What is avg humidity in the month of %s in %s District in state %s. Do not give any textual ans and Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(month,city,state)
        prompt_temp="What is avg Temperature in the month of %s in %s District in state %s.Do not give any textual ans and  Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(month,city,state)
        # prompt_ph="What is avg ph value found in %s. Do not give any textual ans just Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(soil)
        if(month.lower() in rabi_list):
            season=1
        elif(month.lower() in kharif_list):
            season=0
        else:
            season=10        
        if(features[5]==""):
            flag=False
            
        else:
            nitrogen=float(features[5])
            phosphorous=float(features[6])
            potassium=float(features[7])
            flag=True

        # print(prompt_rainfall)
        # print(prompt_ph)
        print(prompt_temp)        

        # completion1 = openai.Completion.create(
        # engine=model_engine,
        # prompt=prompt_rainfall,
        # max_tokens=1024,
        # n=1,
        # stop=None,
        # temperature=0.5,
        # )
        completion2 = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_humidity,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )

        completion3 = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_temp,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )
        # completion4 = openai.Completion.create(
        # engine=model_engine,
        # prompt=prompt_ph,
        # max_tokens=1024,
        # n=1,
        # stop=None,
        # temperature=0.5,
        # )
        # rainfall = float(completion1.choices[0].text)
        humidity = float(completion2.choices[0].text)
        temp = float(completion3.choices[0].text)
        # ph = float(completion4.choices[0].text)
        # print(rainfall)
        # print(ph)
        print(temp)
        print(humidity)
        # print(final1)
        # print(features)
    if flag==True:
        data=pd.read_csv("rainfall.csv")
        df=data[data["DISTRICT"]==city]
        value=np.array(df[month])
        rainfall=value[0]
        ph=ph_list[soil]
        input=[]
        input.append(nitrogen)
        input.append(phosphorous)
        input.append(potassium)
        input.append(temp)
        input.append(humidity)
        input.append(ph)
        input.append(rainfall)
        input.append(season)
        input=np.array(input)
        input=[input]
        value=advancemodel.predict(input)
        ans=crops[value[0]]
        print(ans)
        del input

    else:
        input=[]
        input.append(temp)
        input.append(humidity)
        input.append(ph)
        input.append(rainfall)
        input.append(season)
        input=np.array(input)
        print(input)
        input=[input]
        value=basicmodel.predict(input)
        ans=crops[value[0]]
        print(ans)
        del input

        

    return render_template("prediction.html",crop=ans)

app.run()    