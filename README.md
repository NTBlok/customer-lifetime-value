## PySpark example
### ETL for Metrics Surrounding Customer Lifetime Value from Photo Sharing Events Data

The present `/src` directory includes a data directory that contains python files to create fake event data.  The python module `Faker==0.7.7` was used to create fake data as describe in the file `/src/data/fake_events.py`.  The file `/src/data/run_fake_events.py` creates a random amount within specified limits of fake events.  Global variable `DAYS=14`,  `N_CUSTOMERS=50`, and `MAX_EVENTS=5`.  To keep the data manageable, the timespan time-frame over which the fake events where generated was limited to the most recent 2-3 weeks, max events per customer were set randomly between 1 to 5, and the maximum number of customers in the fake event population were 50. The fake event data is populated to `/input/input.txt`.
To generate the data the following command was run from the `/src` directory:

    $ python data/run_fake_events.py

All PySpark ETL was conducted inside an ipython Jupyter notebook running inside the `jupyter/pyspark-notebook` Docker container previously created and found on DockerHub at `https://hub.docker.com/r/jupyter/pyspark-notebook`

The script used to start the jupyter/pyspark-notebook container is located in the file `/src/start_spark_notebook.sh`.  It mounts the volume of the current working directory so that data is easily uploaded from the input data directory.
The notebook is located in the `/src/notebooks` directory.  To view and edit the notebook, the authentication key is provided at start up and appended to the local host url.  Use of this container is further documented at `https://github.com/jupyter/docker-stacks/tree/master/pyspark-notebook`.  All that is required to start it up, provided Docker is installed and running the followin from the `/src` directory:

    $ ./start_spark_notebook.sh

Output was generated and populated to the `/output` directory from ETL methods inside the spark notebook.  Three output files were deposited there, which provide an visualization of intermediate progress towards the final output of a customer id and customer lifetime value.

All the methods and queries used in the notebook, were exported to the file `/src/methods_pyspark_etl/methods_pyspark_etl.py`.  This file is intended to be the import for testing performed with the `pytest==3.0.6` module and included in the `/src/methods_pyspark_etl/tests` directory. The `/src/methods_pyspark_etl/tests/test_pyspark_etl.py` file is representative of some of the bugs that were found during the process of creating the pyspark notebook and still a work in progress.
