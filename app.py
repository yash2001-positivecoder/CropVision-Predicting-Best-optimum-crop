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

cropdata={"Rice":"Rice is a staple food for over half of the world's population and a cereal grain that originated in China. There are many varieties of rice, including long, medium, and short grain, and it can be cooked in various ways.","Maize":"Maize, also known as corn, is a cereal grain that is one of the most widely cultivated crops in the world. It is a staple food in many countries, especially in Latin America, where it is a major component of the diet","ChickPea":"Chickpeas, also known as garbanzo beans, are a type of legume that are widely grown and consumed around the world.Chickpeas are highly nutritious and are a good source of protein, fiber, and essential vitamins and minerals.","Kidneybeans":"Kidney beans are a type of legume that are widely grown and consumed around the world.Kidney beans are high in protein, fiber, and essential vitamins and minerals, making them a nutritious addition to the diet","pigeonpeas":"Pigeon peas, also known as red gram, are a type of legume that are widely grown and consumed in many countries, particularly in India, Africa, and the Caribbean","Mothbeans":"Moth beans are a type of legume that are grown and consumed in various regions of the world, particularly in India, where they have been part of the local diet for centuries. They are small, round, and have a creamy texture and nutty flavor, making them a versatile ingredient in a variety of dishes","Mungbeans":"Mung beans are a type of legume that are widely grown and consumed in many countries, particularly in Asia, where they have been part of the local diet for thousands of years. They are small, round, and have a delicate texture and slightly sweet flavor, making them a versatile ingredient in a variety of dishes","Blackgram":"Blackgram (Vigna mungo), also known as mung bean, is a legume that is widely grown and consumed in Asia, particularly in India, Bangladesh, and Pakistan. It is a small, oval-shaped, black-skinned seed that has a white, creamy interior and a mild, nutty flavor.","Lentil":"Lentils are small, lens-shaped legumes that come in a variety of colors, including green, brown, red, and yellow. They are a staple food in many cultures and are widely consumed due to their high nutritional value, versatility, and affordability.","Pomegranate":"Pomegranate (Punica granatum) is a fruit that is widely grown and consumed in many parts of the world, particularly in the Mediterranean, Middle East, and Central Asia. It is prized for its juicy, tart-sweet seeds, which are surrounded by a leathery, inedible rind.","Banana":"Bananas are one of the most widely consumed and versatile fruits in the world. They are sweet, creamy, and easy to eat, making them a popular food for people of all ages.","Mango":"Mango (Mangifera indica) is a tropical fruit that is widely grown and consumed in many parts of the world. It is known for its sweet, juicy, and fleshy flesh, which is surrounded by a tough, inedible skin.","Grapes":"Grapes (Vitis vinifera) are a sweet and juicy fruit that is widely grown and consumed in many parts of the world. They come in a variety of colors, including green, red, black, and purple, and are known for their delicate skin and sweet, seed-filled flesh.","Watermelon":"Watermelon (Citrullus lanatus) is a juicy and refreshing fruit that is widely grown and consumed in many parts of the world. It is known for its sweet, juicy flesh and its crisp, refreshing taste.","Muskmelon":"Muskmelon, also known as cantaloupe, is a juicy and sweet fruit that is widely grown and consumed in many parts of the world. It is known for its sweet, juicy flesh, which is surrounded by a tough, inedible rind.","Apple":"Apple is a sweet and juicy fruit that is widely grown and consumed in many parts of the world. It is one of the most popular fruits in the world, known for its crisp texture and sweet, slightly tart flavor.","Orange":"Orange is a juicy and sweet citrus fruit that is widely grown and consumed in many parts of the world. It is known for its bright, orange color and its sweet, tangy flavor.","Papaya":"Papaya is a tropical fruit that is native to Mexico and Central America but is now widely cultivated in many parts of the world. It is a large, tree-like plant that can grow up to 33 feet tall, with a trunk that is typically about 2 feet in diameter.","Coconut":"Coconut is a large, spherical fruit that is produced by the coconut palm, a type of tree that is native to the coastal regions of the Pacific and Indian Oceans. The fruit consists of a hard, outer shell that covers a white, fleshy interior that is surrounded by a sweet, clear liquid known as coconut water.","Cotton":"Cotton is a soft, fluffy fiber that grows around the seeds of the cotton plant, a shrub that is native to tropical and subtropical regions around the world. It is one of the world's most important natural fibers and is widely used in the production of textiles, clothing, and other household items.","Jute":"Jute is a natural fiber that is extracted from the stem of the jute plant, which is native to the Indian subcontinent. It is a long, soft, shiny fiber that is often referred to as the Golden Fiber due to its golden-brown color.","Coffee":"Coffee is a popular beverage made from the roasted seeds of the Coffea plant, which is native to tropical regions in Africa. It is one of the most widely consumed drinks in the world "}

@app.route('/header.html',methods=['POST','GET'])
def home1():
    features1=[x for x in request.form.values()]
    final=[np.array(features1)]
    return render_template("header.html")

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
    global city,month,state,soil,rainfall,humidity,temp,ph,flag,nitrogen,phosphorous,potassium,input,season,prompt_temp,prompt_humidity,ph_list
    
    if(request.method=="POST"):
        features=[x for x in request.form.values()]
        final1=[np.array(features)]
        print(features)
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
        df=data[data["DISTRICT"]==(city.upper())]
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
        d=cropdata[ans]
        crop=ans.lower()
        address="./static/images/%s.jpeg"%(crop)
        print(ans)
        del input

    else:
        data=pd.read_csv("rainfall.csv")
        df=data[data["DISTRICT"]==(city.upper())]
        value=np.array(df[month])
        rainfall=value[0]
        print(rainfall)
        print(soil)
        ph=ph_list[soil]
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
        d=cropdata[ans]
        print(ans)
        crop=ans.lower()
        address="./static/images/%s.jpeg"%(crop)
        del input

        

    return render_template("prediction.html",crop=ans,temp=temp,rain=rainfall,humidity=humidity,add=address,data=d)

app.run()    