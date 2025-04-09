from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_experimental.agents.agent_toolkits.python.base import create_python_agent
import os
load_dotenv()

GROQ_KEY = os.getenv('GROQ')
chat_model = ChatGroq(api_key=GROQ_KEY, model_name="deepseek-r1-distill-llama-70b")

agent_exec = create_python_agent(
    llm=chat_model,
    tool=PythonREPLTool(),
    verbose=True,
    handle_parsing_errors=True
)

def run_agent(initial_prompt):
    response = agent_exec.run(initial_prompt)
    return response

def basic_response(initial_prompt):
    response = chat_model.invoke(initial_prompt)
    return response.content.replace('\n', '').split('</think>')[1]

def generate_response(title, table_content):
    
    # with open(filename, "wb+") as destino:
    #     for chunk in request.FILES['dataset'].chunks():  # Escribir en partes para archivos grandes
    #         destino.write(chunk)
    try:
        """
         Estoy haciendo una aplicacion web, en donde el usuario, y el contenido del archivo se guarda en formato json en un modelo de datos llamado CSVData en la aplicacion llamada 'vslt_app'. Necesito que me ayudes a analizar ese json de la siguiente manera:
        from .models import CSVData
        csv_data = CSVData.objects.get(title='{title}') # Obtiene el registro
        data = csv_data.data_json # Captura la informacion del json en una variable (Cabe recalcar que data ahora es un json pero en formato string)
        df = pd.DataFrame(json.loads(data)) # Convierto el string de json en una tabla 
        
        Si no logras acceder al modelo o hay algun problema, es suficiente con que comprendas que esta es una referencia de la estructura de los datos y campos (te lo enseño en formato json):
        
        """
        llm_response = basic_response(f"""
        Tengo una tabla en csv con las siguientes columnas y con datos de ejemplo:
       {table_content}

        Necesito que analices esa tabla, sus campos, y la estructura de los datos que contiene para entender de que tratan los datos que aborda. Luego de eso, basado en esos campos y datos, dame ideas para hacer graficos de los datos que puedan ser utiles (relacionados con el tema en cuestion, claro). 
        Tu respuesta final debe ser un json que debe seguir unicamente la siguiente estructura por grafico:
        [
            (signo de apertura de llaves)
                "tipo": (tipo de grafico, los tipos de grafico son 'line', 'bar', 'scatter', 'pie', 'histogram'),
                "titulo": "Titulo de grafica 1",
                "fields": ["nombre del campo1 a graficar", "nombre del campo2 a graficar"] # Un array de campos a graficar
            (signo de cierre de llaves),
            
            (signo de apertura de llaves)
                "tipo": (tipo de grafico, los tipos de grafico son 'line', 'bar', 'scatter', 'pie', 'histogram'),
                "titulo": "Titulo de grafica 2",
                "fields": ["nombre del campo1 a graficar", "nombre del campo2 a graficar"] # Un array de campos a graficar
            (signo de cierre de llaves),
            
            (signo de apertura de llaves)
                "tipo": (tipo de grafico, los tipos de grafico son 'line', 'bar', 'scatter', 'pie', 'histogram'),
                "titulo": "Titulo de grafica 3",
                "fields": ["nombre del campo1 a graficar", "nombre del campo2 a graficar"] # Un array de campos a graficar
            (signo de cierre de llaves)
            
            Y asi sucesivamente
        ]
        
        No supongas nada, solo basate en los datos que tienes, si no logras acceder al archivo o hay algun problema, lanza un mensaje de error.          
        """)
    except Exception as e:
        return generate_response(title, table_content)
    
    return llm_response

