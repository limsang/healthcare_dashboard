import os
from mlflow import log_metric, log_param, log_artifact
import mlflow

URI = "http://10.160.210.118:5000/"
if __name__ == "__main__":
    mlflow.set_tracking_uri(URI)
    mlflow.set_experiment("fff")
    
    with mlflow.start_run() as run:
            # Log a parameter (key-value pair)
        mlflow.log_param("param1", 5)

            # Log a metric; metrics can be updated throughout the run
        mlflow.log_metric("foo", 1)
        mlflow.log_metric("foo", 2)
        mlflow.log_metric("foo", 3)

        # Log an artifact (output file)
        with open("output.txt", "w") as f:
            f.write("Hello world!")
        
        mlflow.log_artifacts("output.txt")
        print(mlflow.get_artifact_uri())    
