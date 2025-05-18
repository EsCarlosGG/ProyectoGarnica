from dotenv import load_dotenv
import os
from openai import OpenAI

client = OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

system_rol = '''Haz de cuenta que eres un analizador de sentimeintos.
                 Yo te paso sentimientos y tu analizas el sentimiento de los mensajes
                 y me das una respuesta con al menos 1 caracter y como maximo 4 caracteres
                 SOLO RESPUESTAS NUMERICAS. Donde -1 es negatividad maxima, 0 es neutral y 1 es positividad maxima.
                 Puedes ir entre esos rangos, 0.3, -0.5 etc tambien son validos.
                 (Puedes responder solo con ints o floats)'''                                                            #Esto de aqui es para configurar el sistema
                                                                                                                         #Asi se tiene que comportar la IA (chatgpt)
                                                                                                                         

mensajes = [{"role": "system", "content": system_rol}]          #Hay 3 tipos de sistema: System, User, assistant.
                                                                #Si el "rol" es "User", es lo que el Usuario le esta dando.
                                                                #Rol de "assistant" es la respuesta de la IA, la IA nos da una respuesta de assistant
                                                                #"System" es: como se tiene que comportar la IA, cual es su Rol. por eso en "rol" ponemos: "system"
                                                                
                                                                
class AnalizadorDeSentimientos:
    def analizar_sentimiento(self, polaridad):
        if polaridad > -0.8 and polaridad <= -0.3:
            return "\x1b[1;31m" + "Negativo" + "\x1b[0;37m"                    # "\x1b[0;37m" = Este codigo es para poder darle un color al texto. Se cambia modificando el 31m
        elif polaridad > -0.3 and polaridad < -0.1:
            return "\x1b[1;31m" + "Algo Negativo" + "\x1b[0;37m"
        elif polaridad >= -0.1 and polaridad <= 0.1:
            return "\x1b[1;33m" + "Neutral" + "\x1b[0;37m"
        elif polaridad >= 0.1 and polaridad <= 0.4:
            return "\x1b[1;32m" + "Algo Positivo" + "\x1b[0;37m"
        elif polaridad >= 0.4 and polaridad <= 0.9:
            return "\x1b[1;32m" + "Positivo" + "\x1b[0;37m"
        elif polaridad > 0.9:
            return "\x1b[1;32m" + "Muy Positivo" + "\x1b[0;37m"
        else:
            return "\x1b[1;31m" + "Muy Negativo" + "\x1b[0;37m"
        
analizador = AnalizadorDeSentimientos()

while True:
    user_prompt = input("\x1b[1;33m" + "\nDime Algo: "  + "\x1b[0;37m")         #Esto es lo que esta escribiendo el usuario
    mensajes.append({"role": "user", "content": user_prompt})                   #Todo lo que el ususario escribe, se lo pasamos en "user" = "role": "user"        /    Cada que se escriba algo, vamos a agregar un nuevo rol ("user") que va a tener el contenido de lo que el usuario escriba
    
    completion = client.chat.completions.create(                                  #Esto es para autocompletar el chat con respuestas de la IA
        model = "gpt-3.5-turbo",
        messages = mensajes,
        max_tokens = 8
    )
    
    
    #Ahora tenemos que agregar la respuesta del modelo, para que despues tenga sus propias respuesta en concideracion
    respuesta = completion.choices[0].message.content
    mensajes.append({"role": "assistant", "content": respuesta})                   #Estamos agregando la respuesta que nos da el chatbot
    
    sentimiento = analizador.analizar_sentimiento(float(respuesta))
    print(sentimiento)