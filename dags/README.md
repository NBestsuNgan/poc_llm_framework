# Control Flow

## Table of Contents
- [Control Table](#control-table)
- [Orchestrator](#orchestrator)
- [Process Flow](#process-flow)



### Control Table

![control_table](/resource/iamges/control_flow/control_table.png "Control table")

The framework includes **7 control tables**, each serving a different configuration or orchestration purpose:

1. **CNTL_AF.CNTL_CFG_STREM**  
   ![CNTL_CFG_STREM](/resource/iamges/control_flow/cntl_strem.png "CNTL_CFG_STREM")  
   - Registers the *stream name* of a workflow. Each workflow (stream) can contain multiple process groups.

2. **CNTL_AF.CNTL_CFG_PRCS_GRP**  
   ![CNTL_CFG_PRCS_GRP](/resource/iamges/control_flow/cntl_prcs_grp.png "CNTL_CFG_PRCS_GRP")  
   - Registers *process groups* within a workflow stream. Each process group can contain multiple processes.

3. **CNTL_AF.CNTL_CFG_PRCS**  
   ![CNTL_CFG_PRCS](/resource/iamges/control_flow/cntl_prcs.png "CNTL_CFG_PRCS")  
   - Registers individual *processes*. Ideally, each process group should have only one main process for clarity.

4. **CNTL_AF.CNTL_CFG_SYS_FILE**  
   ![CNTL_CFG_SYS_FILE](/resource/iamges/control_flow/cntl_sys_file.png "CNTL_CFG_SYS_FILE")  
   - Registers the *system file type* associated with each process. Each process should be linked to only one system file.

5. **CNTL_AF.CNTL_CFG_PRCS_DEPN**  
   ![CNTL_CFG_PRCS_DEPN](/resource/iamges/control_flow/cntl_depn.png "CNTL_CFG_PRCS_DEPN")  
   - Registers *process dependencies*. Each process can depend on multiple other processes, but cannot depend on itself.

6. **CNTL_AF.CNTL_CFG_SCHEDULE**  
   ![CNTL_CFG_SCHEDULE](/resource/iamges/control_flow/cntl_schedule.png "CNTL_CFG_SCHEDULE")  
   - Registers the *schedule time* for each workflow.

7. **CNTL_AF.CNTL_CFG_LOG**  
   ![CNTL_CFG_LOG](/resource/iamges/control_flow/cntl_log.png "CNTL_CFG_LOG")  
   - Logs the *execution status* (e.g., success or error) of each process, including any relevant messages.

---

### Orchestrator

> The orchestrator—managed by **Apache Airflow**—acts as the controller that reads metadata from the control tables to execute and monitor each process. It handles scheduling, triggering, and logging.

This framework defines **two types of DAGs**:

1. **Stream-type DAGs**  
   These DAGs control the execution of *process groups* based on their priority and structure. They handle orchestration at a higher level across grouped processes.

   ![stream_dag](/resource/iamges/control_flow/stream_dag.png "stream_dag")  
   - The diagram shows how a stream DAG manages the overall execution of processes within each process group, respecting priorities.

2. **Process-type DAGs**  
   These DAGs focus on executing individual *notebooks or scripts*, ensuring that all dependencies are met before execution.

   ![process_dag](/resource/iamges/control_flow/process_dag.png "process_dag")  
   - The diagram shows how a process DAG waits for dependent processes before executing its own logic.

Together, these two DAG types work in tandem to fully orchestrate workflows from grouped streams down to individual processing units.


## Process Flow

To run a complete pipeline in this framework, the user needs to interact with **four main components**, as illustrated in the diagram:

- **1. PostgreSQL (via DBeaver):**  
  The user manually registers configuration and metadata parameters into PostgreSQL using a database client such as DBeaver.

- **2. Apache Airflow (DAG definition):**  
  A DAG Python file (`dag.py`) must be created locally in `dags` folder within the designated folder so Apache Airflow can detect and orchestrate the pipeline.

- **3. Jupyter Notebook Container:**  
  The user must develop the required notebook(s) in the Jupyter environment. Each notebook represents a modular step in the pipeline.

- **4. AI Agent (via ADK):**  
  AI Agents are developed and tested locally using the Agent Development Kit (ADK), then integrated into the Jupyter Notebook container.

---

![Process Flow](/resource/iamges/control_flow/process_flow.png "Process Flow")

The diagram above shows the process flow of the framework.

1. **Parameter Initialization**  
   Parameters are read from PostgreSQL, which serves as both a configuration and metadata database. These parameters are passed into Apache Airflow, the orchestrator.

2. **Airflow Orchestration**  
   Apache Airflow receives parameters from PostgreSQL to manage the workflow. It then passes these parameters into the Jupyter Notebook container. Each process in Airflow can freely select and trigger any notebook within the Jupyter environment.

3. **Notebook Execution**  
   The selected Jupyter Notebook can receive parameters sent from Apache Airflow. It is also capable of communicating with AI Agents that are registered via the Agent Development Kit (ADK), which is developed and tested locally.

4. **AI Agent Integration**  
   AI Agents are first developed and tested locally using the ADK. Once ready, they are registered to the Jupyter Notebook container. Each AI Agent can be freely reused and invoked across different notebooks.


---