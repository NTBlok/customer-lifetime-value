#docker run -it --rm -p 8888:8888 -v $(dirname $(pwd)):/home/jovyan/work   --name pyspark-etl jupyter/pyspark-notebook
docker run -it --rm -p 8888:8888 -v $(dirname $(pwd)):/home/jovyan/work   --name pyspark-etl jupyter/pyspark-notebook-pytest
