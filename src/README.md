## PySpark ETL for Metrics Surrounding Customer Lifetime Value

The present `/src` directory includes a data directory that contains python files to create fake data similar to that in the sample_input directory above.  The python module `Faker==0.7.7` was used to create fake data as describe in the file `data/fake_events.py`.  The file `data/run_fake_events.py` creates a random amount within specified limits of fake events.  Global variable `DAYS=14`,  `N_CUSTOMERS=50`, and `MAX_EVENTS=5`.  To keep the data manageable, the timespan time-frame over which the fake events where generated was limited to the most recent 2-3 weeks, max events per customer were set randomly between 1 to 5, and the maximum number of customers in the fake event population were 50.
To generate the data the following command was run:

    $ python data/run_fake_events.py

All PySpark ETL was conducted inside an ipython Jupyter notebook running inside the `jupyter/pyspark-notebook` Docker container previously created and found on DockerHub at `https://hub.docker.com/r/jupyter/pyspark-notebook`

The script used to start the jupyter/pyspark-notebook container is located in the file `start_spark_notebook.sh`.  It mounts the volume of the current working directory so that data is easily uploaded from the data directory.
The notebook is located in the `notebooks` directory.  To view and edit the notebook, the authentication key is provided at start up and appended to the local host url.  Use of this container is further documented at `https://github.com/jupyter/docker-stacks/tree/master/pyspark-notebook`.  All that is required to start it up, provided Docker is installed and running is the following:

    $ ./start_spark_notebook.sh

Output was generated and populated in the desired output directory located above the src from ETL methods inside the spark notebook.  Three output files were deposited there, which provide an visualization of intermediate progress towards the final output of a customer id and customer lifetime value.

All the methods and queries used in the notebook, were exported to the file `methods_pyspark_etl.py`.  This file is intended to be the import for documented testing performed with the `pytest==3.0.6` module and included in the `/tests` directory.  Ad hoc testing was consistently performed through the creation of the pyspark notebook.  The `/tests` directory is a representative of some of the bugs that were found during the process of creating the pyspark notebook and for further work, it is where I would spend more of my future time in this endeavor.
