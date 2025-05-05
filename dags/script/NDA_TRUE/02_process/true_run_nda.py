from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
from framework.framework import Framework
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
import subprocess
from airflow.operators.empty import EmptyOperator
from functools import partial

controller = Framework.get_controller("true_run_nda", 'prcs_nm')

default_args = {
    'owner': f"{controller.owner}-process",
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

def CheckSuccessGroupOfProcess(group_process, data_dt):
    Framework.Utility.CheckSuccessGroupOfProcess(group_process, data_dt)

with DAG(
    dag_id='true_run_nda',
    default_args=default_args,
    start_date = controller.calc_dt,
    schedule_interval=None,
) as dag:
    # false mean process not run yet
    # true mean process not run already in specifc condition
    # check if process has runned? if no(false) --> check it depend and execute it --> after that 
    # insert log with status = 1 --> execute it if success update log with status = 0 else update log with status = 99
    def TriggerDependenciesProcess():
        trigger_tasks = []
        if controller.dpnd_prcs_nm[0] is not None:
            for dep_dag in range(len(controller.dpnd_prcs_nm)):
                depn_controller = Framework.get_controller(f"{controller.dpnd_prcs_nm[dep_dag]}", 'prcs_nm')
                if depn_controller.prcs_act_f[0] == 1 and controller.depn_act_f[dep_dag] == 1:
                    trigger_task = TriggerDagRunOperator(
                        task_id=f'trigger_dependency_{controller.dpnd_prcs_nm[dep_dag]}',
                        trigger_dag_id=controller.dpnd_prcs_nm[dep_dag],
                        dag=dag,  # Associate with the DAG
                    )
                    trigger_tasks.append(trigger_task)
            
            check_success_group_of_process = PythonOperator(
                    task_id=f'check_success_group_of_process_trigger_dependency_{controller.dpnd_prcs_nm[dep_dag]}',
                    python_callable=partial(CheckSuccessGroupOfProcess, controller.dpnd_prcs_nm[dep_dag], datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
                    dag=dag,
                )
            trigger_tasks.append(check_success_group_of_process)
        return trigger_tasks

    container_id = Framework.Utility.GetContainerId()    

    def execute_notebook():
        if controller.go_live == 1:
            date_run = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            date_run = datetime.strptime(controller.data_dt, "%Y-%m-%d").replace( hour=0, minute=0, second=0, microsecond=0)

        data_dt=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cal_dt = datetime.now()
        server_link = "http://localhost:8888/tree/notebooks"
        Framework.Utility.InsertLogProcess(controller.prcs_nm, data_dt, cal_dt, cal_dt, 1)     

        command = f"""
            docker exec {container_id} bash -c "
            mkdir -p /home/jovyan/notebooks/Log_output/{controller.prcs_nm} &&
            papermill /home/jovyan/notebooks/{controller.nb_path_nm} \
            /home/jovyan/notebooks/Log_output/{controller.prcs_nm}/{controller.nb_path_nm.split('/')[-1].replace('.ipynb','_executed.ipynb')} \
            -p nb_parm '{controller.nb_parm}' \
            -p date_run '{date_run}' \
            -p model '{controller.model}' 
        "
        """

        try:
            subprocess.run(command, shell=True, check=True)
            Framework.Utility.UpdateLogProcess(controller.prcs_nm, data_dt, cal_dt, datetime.now(), 0, f"Success run at {datetime.now()}")     
            print(f"Success Running : {server_link}/Log_output/{controller.prcs_nm}/{controller.nb_path_nm.split('/')[-1].replace('.ipynb','_executed.ipynb')}")
        except subprocess.CalledProcessError as e:
            Framework.Utility.UpdateLogProcess(controller.prcs_nm, data_dt, cal_dt, datetime.now(), 99, f"{server_link}/{controller.nb_path_nm}")     
            raise Exception(f"{e} \nFailed to run, Log-Error-Path:  {server_link}/Log_output/{controller.prcs_nm}/{controller.nb_path_nm.split('/')[-1].replace('.ipynb','_executed.ipynb')} \
                            \n Primitive-Path: {server_link}/{controller.nb_path_nm}")

    ExecuteNotebook = PythonOperator(
        task_id='ExecuteNotebook',
        python_callable=execute_notebook,
    ) 

    TriggerDependencyTasks = TriggerDependenciesProcess()
    TriggerDependencyTasks  >> ExecuteNotebook 
    