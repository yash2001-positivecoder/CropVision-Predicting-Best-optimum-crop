import openai
import pickle
import numpy as np
openai.api_key = "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"
model_engine = "text-davinci-003"
city=input("Enter city: ")
month=input("Enter Month: ")
state=input("Enter the state:")
soil=input("Enter the soil type: ")
prompt_rainfall = "What is avg rainfall in the month of %s in %s District in state %s. Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(month,city,state)
prompt_humidity="What is avg humidity in the month of %s in %s District in state %s. Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(month,city,state)
prompt_temp="What is avg Temperature in the month of %s in %s District in state %s. Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(month,city,state)
prompt_ph="What is avg ph value found in %s soil. Give me ans in number only.Convert your ans into single number only.Remove the unit from the ans"%(soil)
basicmodel=pickle.load(open('basic_model.pkl','rb'))
print(prompt_rainfall)
completion1 = openai.Completion.create(
    engine=model_engine,
    prompt=prompt_rainfall,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)
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
completion4 = openai.Completion.create(
    engine=model_engine,
    prompt=prompt_ph,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)


rainfall = float(completion1.choices[0].text)
humidity = float(completion2.choices[0].text)
temp = float(completion3.choices[0].text)
ph = float(completion4.choices[0].text)

print(type(rainfall))
# rain=float(rainfall)
# print(type(rain))
season=0
input=[]
input.append(temp)
input.append(humidity)
input.append(ph)
input.append(rainfall)
input.append(season)
crops={1:"Rice",2:"Maize",3:"ChickPea",4:"Kidneybeans",5:"pigeonpeas",6:"Mothbeans",7:"Mungbeans",8:"Blackgram",9:"Lentil",10:"Pomegranate",11:"Banana",12:"Mango",13:"Grapes",14:"Watermelon",15:"Muskmelon",16:"Apple",17:"Orange",18:"Papaya",19:"Coconut",20:"Cotton",21:"Jute",22:"Coffee"}
input=np.array(input)
input=[input]
# print(input.shape)
value=basicmodel.predict(input)
print(value)
print(type(value))
print(crops[value[0]])
print("\nRainfall:",rainfall)
print("humidity: ",humidity)
print("Temp: ",temp)
print("ph: ",ph)
# print("Nitrogen: ",nitrogen)