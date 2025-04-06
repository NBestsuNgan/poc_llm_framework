from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor

from datetime import datetime, timedelta
from framework.framework import Framework
import sys, os, subprocess
from functools import partial

strem_controller = Framework.get_controller("Brids_strem", 'strem_nm')

default_args = {
    'owner': f"{strem_controller.owner}-stream",
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

def check_success(process_name, data_dt):
    Framework.Utility.CheckSuccess(process_name, data_dt)

with DAG(
    dag_id = 'Brids_strem',
    default_args = default_args,
    start_date = strem_controller.calc_dt,
    schedule_interval = strem_controller.cron_express,
) as dag:    


    def create_trigger_tasks():
        #get prcs_nm by order but trigger all at once
        trigger_tasks = []
        for prcs_grp in range(len(strem_controller.prcs_grp)):
            if strem_controller.prcs_grp_act_f[prcs_grp] != 0:
                prcs_grp_controller = Framework.get_controller(f"{strem_controller.prcs_grp[prcs_grp]}", 'prcs_grp')
                for prcs_nm in range(len(prcs_grp_controller.prcs_nm)):
                    if prcs_grp_controller.prcs_act_f[prcs_nm] != 0:
                        trigger_task = TriggerDagRunOperator(
                            task_id=f'Trigger_{prcs_grp_controller.prcs_nm[prcs_nm]}_{prcs_grp_controller.prcs_grp[prcs_nm]}_{strem_controller.prcs_grp_prir[prcs_grp]}_{prcs_grp_controller.prcs_prir[prcs_nm]}',
                            trigger_dag_id=prcs_grp_controller.prcs_nm[prcs_nm],
                            dag=dag,  # Associate with the DAG strem level
                        )
                        trigger_tasks.append([trigger_task])

                        check_success_task = PythonOperator(
                            task_id=f'check_success_{prcs_grp_controller.prcs_nm[prcs_nm]}',
                            python_callable=partial(check_success, prcs_grp_controller.prcs_nm[prcs_nm], datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
                            dag=dag,
                        )
                        trigger_tasks.append([check_success_task])

        return trigger_tasks

    trigger_tasks = create_trigger_tasks()


    # Set dependencies dynamically
    for i in range(len(trigger_tasks) - 1): 
        for task in trigger_tasks[i]: 
            for next_task in trigger_tasks[i + 1]:
                task >> next_task

    # last_phase_tasks = trigger_tasks[len(trigger_tasks) - 1]
    # for task in last_phase_tasks:
    #     task >> print_message
