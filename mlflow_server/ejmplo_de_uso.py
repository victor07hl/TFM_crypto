# %% [markdown]
# # Importing Libraries

# %%
import mlflow
from mlflow.exceptions import RestException
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn import tree

# %% [markdown]
# # Setting the mlflow url

# %%
remote_server_uri = "http://34.58.215.162:8080/"  # set to your server URI
mlflow.set_tracking_uri(remote_server_uri)

# %% [markdown]
# # Creating Experiment
# or getting the id if already exists

# %%
try:
    experiment_name = 'experimentgcp' #Puede ser cualquiera siempre y cuando no se troque con otro
    experiment_id = (mlflow
                        .create_experiment(name=experiment_name
                                            ,tags={'created_by':'Victor Moreno','other_tag':'other'})) #importante poner el nombre de quien lo crea
except RestException as r:
    print(r) #por si ya existe ps se trabaja sobre ese 
    experiment = mlflow.get_experiment_by_name(experiment_name)
    print('Full name',experiment.name)
    experiment_id = experiment.experiment_id

# %% [markdown]
# # Aqui inicia el entrenamiento 
# la idea es colocar la parte del entrenamiento dentro del contexto de mlflow.start_run
# aunque la idea es registrar el modelo entrenado nomas y las metricas la siguiente celda tiene un ejemplo basico

# %%
#como ejemplo dejo la parte de cargar aparte , para evitar confusiones de que todo lo relacionado 
#a la ejecucion debe quedar dentro del contexto

#Cargando la data y procesandola
# load dataset and train model
iris = load_iris()

# %%
with mlflow.start_run(experiment_id=experiment_id,
                     run_name='run1') as run:
    
    #instantiating the DecisionTreeClassifier
    sk_model = tree.DecisionTreeClassifier()
    sk_model = sk_model.fit(iris.data, iris.target) 

    # log model params
    #Los parametros , lo recomendado es poner hiperparametros del modelo o bueno parametros 
    # el concepto de mlflow es poner los parametros utilizados para entrenar el modelo y de esta forma ir comparando 
    # y ajustando basado en las metricas 
    mlflow.log_param("criterion", sk_model.criterion)
    mlflow.log_param("splitter", sk_model.splitter)

    #este es requisito para cuando se registra el modelo que no vamos hacer registro de modelos por ahora 
    #sin embargo ayuda como guia para cuando querramos usar el modelo entrenado para hacer inferencias
    signature = infer_signature(iris.data, sk_model.predict(iris.data))

    # log model
    mlflow.sklearn.log_model(sk_model, "sk_models", signature=signature)

    #Guardando metricas
    mlflow.log_metric('MAE',0.00002)
    mlflow.log_metric('mse',0.03)

    #metricas y parametros pueden ser guardados con un solo comando 
    mlflow.log_metrics({'metric1':0.7,'metric2':0.08})
    mlflow.log_params({'param1':'value1','param2':'value2'})

    #guardando imagenes de evidencia 
    mlflow.log_artifact('result.png')
    mlflow.log_artifact('result2.png')


# %% [markdown]
# # Nested runs
# por si se necesita 
# 

# %% [markdown]
# with mlflow.start_run(experiment_id=experiment_id, run_name='parent_run') as p_run:
#     with mlflow.start_run(experiment_id=experiment_id, run_name='child_run') as c_run:
# 
#         #put your code here 
