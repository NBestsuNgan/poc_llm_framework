# LLm Local Framework

# Table of content
- [Introduciton](#Introduciton)
- [Services Use](#Services-Use)
- [Components of Framework ](#Components-of-Framework )
- [Set up environment](#Set-up-environment)
- [Reference](#Reference)


# Introduciton
#### Project purpose
 > This framework was build for perform task on specific business task group like merchandise recommendation, etc. with specific framework structure pattern which will show later. the framework bring Llm into loop for extract reasoning of llm based on provided data or as we already know in the name 'RAG' also try other technique which be useful as well.
 

# Services Use
![services_use](resource/iamges/services_use.png "Services Use") 

&nbsp; FrFrom picture above there are 5 main services involve in this porject hosted on docker each serivces serve as different purpose but work along together.om 

# Components of Framework 

### Control table

![control_table](resource/iamges/control_table.png "Control table")

&nbsp; Control tables have 6 control table which server different purpose
- 1.CNTL_AF.CNTL_CFG_STREM
   ![CNTL_CFG_STREM](resource/iamges/CNTL_CFG_STREM.png "CNTL_CFG_STREM")
   - used for register strem name of workflow, by each workflow can have many process group.
- 2.CNTL_AF.CNTL_CFG_PRCS_GRP
   ![CNTL_CFG_PRCS_GRP](resource/iamges/CNTL_CFG_PRCS_GRP.png "CNTL_CFG_PRCS_GRP")
   - used for register process group in a stream workflow, by each process group can have many process.
- 3.CNTL_AF.CNTL_CFG_PRCS
   ![CNTL_CFG_PRCS](resource/iamges/CNTL_CFG_PRCS1.png "CNTL_CFG_PRCS")
   ![CNTL_CFG_PRCS](resource/iamges/CNTL_CFG_PRCS2.png "CNTL_CFG_PRCS")
   - used for register process, by each process can be store in many process group
- 4.CNTL_AF.CNTL_CFG_PRCS_DEPN
   ![CNTL_CFG_PRCS_DEPN](resource/iamges/CNTL_CFG_PRCS_DEPN.png "CNTL_CFG_PRCS_DEPN")
   - used for register process dependency, by each process can have many depend process but cannot depend itself.
- 5.CNTL_AF.CNTL_CFG_SCHEDULE
   ![CNTL_CFG_SCHEDULE](resource/iamges/CNTL_CFG_SCHEDULE.png "CNTL_CFG_SCHEDULE")
   - used for register workflow schedule time.
- 6.CNTL_AF.CNTL_CFG_LOG
   ![CNTL_CFG_LOG](resource/iamges/CNTL_CFG_LOG.png "CNTL_CFG_LOG")
   - used for logging process status like sucess or error inclusive with message.

### Orchestrator 
![frameword_architecture](resource/iamges/frameword_architecture.png "frameword_architecture")

&nbsp; Orchestrator(apache-airflow) is directly associate with the control table by pulling config data from control table then dynamically generate task that associate with config in control table order by process group/process task priority as shown in picture below

##### Stream Dag 
![stream_dag](resource/iamges/stream_dag.png "stream_dag")

&nbsp; In stream dag we will divide process based on it process group and process priority 

##### Process Dag
![process_dag2](resource/iamges/process_dag2.png "process_dag2")

&nbsp; In process will have two major task which is trigger it dependency and execute notebook from notebook path configuration

### Processing & Clustering and Data lakehouse & Data warehouse 
#### Datalakehouse and warehouse architecture
![laekhouse_warehouse_architecture](resource/iamges/laekhouse_warehouse_architecture.png "Airflow UI")

&nbsp; From picture above we can see that this picture consists of 3 services: 
   -  Processing&Clustering: reponsible by <span style="color:red;">spark-iceberg</span> services by combining spark that act like processing unit and iceberg 
      which is Open-Table-Fomat(OTFs) as a solution that leverages distributed computing and distributed object stores to 
      provide capabilities that exceed what is possible with a Data Warehouse .
   -  Data lakehouse: reponsible by <span style="color:red;">minio</span> act like blob files storage like amazon s3, you can store any data in any format in minio.
   -  Data warehouse: reponsible by <span style="color:red;">oracle(PDB-->portable database)</span> act like data warehouse to store data in structural format.



# Data tier concept
&nbsp; Data tier concept is most commonly use in data processing framework project, this concept can enhance data management easier by improve
observabiliy, loging, tracking and data organization 

#### Data tier1
![framework_tier1](resource/iamges/framework_tier1.png "Airflow UI")

&nbsp; tier1 of data management is for make procedure to control all process that coming to this loop, generally tier1 is defied as transform any 
data format from various source into staging layer which format is structure format



#### Data tier2
![framework_tier2](resource/iamges/framework_tier2.png "Airflow UI")

&nbsp; tier2 of data management is to transform staging layer into up tier like Dimention or Fact table, typically is to direct load data and table format from
staging layer into Dimention or Fact table directly but we can do some transformation if need.

#### Data tier3
![framework_tier3](resource/iamges/framework_tier3.png "Airflow UI")

&nbsp; tier3 of data management is to do some aggregation from Dimention and Fact table, you do some thing like sum, group by,
join and much more.

# Set up environment
-  Set up Oracle Database (PDB) for macos
   -  follow the link to install oracle on macos, you may need to extend memory or disk usage in docker: https://www.youtube.com/watch?v=uxvoMhkKUPE
   -  problem with restricted mode run as follow (optional)
      - docker exec -it oracle19 bash
      - sqlplus sys/mypassword1@localhost:1521/ORCLCDB AS SYSDBA
      - ALTER SYSTEM DISABLE RESTRICTED SESSION;
      - ctrl + D to exit sql mode, same with bash mode
   - grant privilege
      `GRANT UNLIMITED TABLESPACE TO sys`
      
   ***Note: you need to wait for few minute(up to 5 minutes for CDB mode and 8 minutes for PDB mode) to let the oracle finished it initialization and leave restrict mode, then you will fully connect to the database***

-  Download postgres database
   -  you need to install database for using postgres(same as oracle) https://www.postgresql.org/download/ 
   -  after installed the image in docker compose file will do it job.

-  Dockerfile setup for spark-iceberg image
   -  ```docker build -t jupyter/base-notebook:latest . ```
   -  this container will act like processing and clustering unit, you can append more python module via add it into **requirements.txt** after added you need to re-build the image again.



# How to start it? 
-  after the setup spark-iceberg image and oracle image already, you can simply run ```docker compose up -d ``` to start all container, the left image will automatically download to your computer.
-  build new process by using this command to create new template with variable --env script/PRCS_TEST_FRAMEWORK4.py --build ```./dags/framework/app.sh --env script/PRCS_TEST_FRAMEWORK4.py --build```


# Reference
Ref for stylish design : 
   - https://www.reddit.com/r/dataengineering/comments/124wcjb/my_3rd_data_project_with_airflow_docker_postgres/

 


 