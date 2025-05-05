from datetime import datetime, timedelta 
from enum import Enum
import re, sys, os, subprocess, json
from types import ModuleType
from typing import Dict, List, Any
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from croniter import croniter 
import time


class Framework(ModuleType):
    class Controller:
        args: Dict[str, Any]

        strem_nm: str
        data_dt: str
        go_live: str
        prcs_grp: list
        prcs_grp_prir: str
        prcs_grp_act_f: list
        cron_express : str
        owner : str

        prcs_nm: list
        prcs_prir: list
        sys_file: str
        sys_file_parm: str
        model: list
        nb_path_nm: str
        nb_parm: str
        prcs_act_f: list
        dpnd_prcs_nm: list
        depn_chk: int
        depn_act_f: list
        calc_dt : datetime
        
 
        collection : str

        def __init__(self, args: dict, flag_type):
            if flag_type == 'strem_nm':
                self.strem_nm = args['strem_nm']
                self.data_dt = args['data_dt']
                self.go_live = args['go_live']
                self.prcs_grp = args['prcs_grp']
                self.prcs_grp_prir = args['prcs_grp_prir']
                self.prcs_grp_act_f = args['prcs_grp_act_f']
                self.cron_express = args['cron_express']
                self.owner = args['owner']
                self.calc_dt =  croniter(args['cron_express'], datetime.now()).get_prev(datetime)
            elif flag_type == 'prcs_grp':
                self.prcs_grp = args['prcs_grp']
                self.prcs_nm = args['prcs_nm']
                self.prcs_prir = args['prcs_prir']
                self.prcs_act_f = args['prcs_act_f']
            elif flag_type == 'prcs_nm':
                self.prcs_nm = args['prcs_nm'][0]
                self.prcs_grp = args['prcs_grp']
                self.prcs_prir = args['prcs_prir']
                self.sys_file = args['sys_file']
                self.sys_file_parm = args['sys_file_parm']
                self.model = args['model']
                self.nb_path_nm = args['nb_path_nm']
                self.nb_parm = args['nb_parm']
                self.prcs_act_f = args['prcs_act_f']
                self.dpnd_prcs_nm = args['dpnd_prcs_nm']
                self.depn_act_f = args['depn_act_f']
                self.data_dt = args['data_dt']
                self.go_live = args['go_live']
                self.owner = args['owner']
                self.calc_dt = croniter(args['cron_express'], datetime.now()).get_prev(datetime)
            
    class InitController(Controller):
        def __init__(self, args: dict, flag_type):
            if len(args) != 0:
                super().__init__(args, flag_type)

    @classmethod
    def get_controller(self, flag_value: str = None, flag_type: str = None) -> Controller:
        # purpose is to call init of controller
        #1.retrieve config from postgres
            #fetchone(): Fetches a single row from the result set.
            #fetchall(): Fetches all rows from the result set.
            #fetchmany(size): Fetches a specified number of rows from the result set.
        conn = Framework.Utility.GetConnection()
        cusor = conn.cursor()
        if flag_type == 'strem_nm':
            cusor.execute(f"""select 
                            strem.strem_nm
                            , strem.data_dt
                            , strem.go_live
                            , prcs_grp.prcs_grp
                            , prcs_grp.prir as prcs_grp_prir
                            , prcs_grp.act_f as prcs_grp_act_f
                            , COALESCE(strem.strem_owner, 'test-framework') as owner
                            , concat(schedule.minutes, ' ', schedule.hours, ' ', schedule.day_month, ' ', schedule.months, ' ', schedule.day_week) as cron_express
                            from cntl.cntl_cfg_strem strem
                            left join cntl.cntl_cfg_prcs_grp prcs_grp  
                                on strem.strem_nm = prcs_grp.strem_nm 
                            left join cntl.cntl_cfg_schedule schedule
                                on strem.strem_nm = schedule.strem_nm 
                            where strem.strem_nm = '{flag_value}' and prcs_grp.act_f <> 0
                            order by prcs_grp_prir                 
                            """)
        elif flag_type == 'prcs_grp':
            cusor.execute(f"""select 
                            prcs_grp.prcs_grp 
                            , prcs.prcs_nm 
                            , prcs.prir as prcs_prir
                            , prcs.act_f as prcs_act_f
                            from cntl.cntl_cfg_prcs_grp prcs_grp 
                            left join  cntl.cntl_cfg_prcs prcs 
                                on prcs_grp.prcs_grp = prcs.prcs_grp
                            where prcs.prcs_grp = '{flag_value}'
                            order by prcs_prir
                            """)
        elif flag_type == 'prcs_nm':
                       cusor.execute(f"""select 
                            prcs.prcs_nm
                            , prcs.prcs_grp
                            , prcs.prir as prcs_prir
                            , prcs.sys_file 
                            , prcs.model
                            , prcs.nb_path_nm
                            , prcs.nb_parm
                            , prcs.act_f as prcs_act_f
                            , depn.dpnd_prcs_nm
                            , depn.act_f as depn_act_f
                            , concat(sys_file.file_type, '|', sys_file.dlm, '|', sys_file.chunk_size, '|', sys_file.overlap) as sys_file_parm
                            , strem.data_dt  
                            , strem.go_live  
                            , COALESCE(strem.strem_owner, 'test-framework') as owner
                            , concat(schedule.minutes, ' ', schedule.hours, ' ', schedule.day_month, ' ', schedule.months, ' ', schedule.day_week) as cron_express
                            from cntl.cntl_cfg_prcs prcs   
                            left join cntl.cntl_cfg_prcs_depn depn
                                on prcs.prcs_nm = depn.prcs_nm 
                            left join cntl.cntl_cfg_prcs_grp prcs_grp 
                                on prcs.prcs_grp = prcs_grp.prcs_grp 
                            left join cntl.cntl_cfg_strem strem
                                on prcs_grp.strem_nm = strem.strem_nm
                            left join cntl.cntl_cfg_schedule schedule
                                on strem.strem_nm = schedule.strem_nm
                            left join cntl.cntl_sys_fle sys_file
                                on prcs.sys_file = sys_file.sys_nm
                            where prcs.prcs_nm = '{flag_value}'
                            """)
                       
        header_row = [i[0] for i in cusor.description]
        data_row = cusor.fetchall() # [(),(), ...]

        #2.connect arttribute by joining and conbine to json or dict format configuration pass
        config_data = dict()
        for hr_ind in range(len(header_row)):
            for dr_ind in range(len(data_row)): 
                if header_row[hr_ind] in ('prcs_grp','prcs_nm','dpnd_prcs_nm','prcs_grp_act_f', 'prcs_act_f', 'depn_act_f','prcs_prir','prcs_grp_prir') and  header_row[hr_ind] not in config_data:
                    config_data[header_row[hr_ind]] = [data_row[dr_ind][hr_ind]]
                elif header_row[hr_ind] in ('prcs_grp','prcs_nm','dpnd_prcs_nm','prcs_grp_act_f', 'prcs_act_f', 'depn_act_f','prcs_prir','prcs_grp_prir') and  header_row[hr_ind] in config_data:
                    config_data[header_row[hr_ind]].append(data_row[dr_ind][hr_ind])
                elif header_row[hr_ind] not in config_data:
                    config_data[header_row[hr_ind]] = data_row[dr_ind][hr_ind]

        #3.initial config of airflow dag
        # return config_data
        return Framework.InitController(config_data, flag_type)


    class Utility(ModuleType):
        @classmethod
        def GetConnection(self):
            hook = PostgresHook(postgres_conn_id='postgres_localhost')
            conn = hook.get_conn()
            return conn
        
        @classmethod
        def CheckSuccessGroupOfProcess(self, group_process, data_dt):
            conn = Framework.Utility.GetConnection()
            time.sleep(5)
            cusor = conn.cursor() 
            placeholders = ', '.join(['%s'] * len(group_process))
            attempt = 1
            check_query = f"""
                SELECT prcs_nm, status FROM cntl.cntl_cfg_log
                WHERE prcs_nm IN ({placeholders}) AND data_dt = %s
            """

            # Flatten values into a tuple: (*group_process, data_dt)
            values = tuple(group_process) + (data_dt,)
            while True:
                cusor.execute(check_query, values)
                conn.commit() 


                header_row = [i[0] for i in cusor.description]
                data_row = cusor.fetchall() # [(),(), ...]
                all_complete = 0
                for hr_ind in range(len(header_row)):
                    for dr_ind in range(len(data_row)): 
                        if header_row[hr_ind] == 'status' and data_row[dr_ind][hr_ind] == 0:
                            all_complete += 1
                            print(f"attempt#{attempt} process : {data_row[dr_ind][0]} is success")
                        elif header_row[hr_ind] == 'status' and data_row[dr_ind][hr_ind] == 1:
                            print(f"attempt#{attempt} process : {data_row[dr_ind][0]} is running")
                        elif header_row[hr_ind] == 'status' and data_row[dr_ind][hr_ind] == 99:
                            raise Exception(f"Process: {data_row[dr_ind][0]} have failed")
                print('########################################')
                if all_complete == len(data_row):
                    print('All tasks are complete!')
                    break

                attempt += 1 
                time.sleep(10)


        @classmethod
        def InsertLogProcess(self, process_name, data_dt, start_dt, end_dt, status, message='', source_row=0, target_row=0):
            conn = Framework.Utility.GetConnection()
            cusor = conn.cursor() 
            check = """
                    select * from cntl.cntl_cfg_log
                    where prcs_nm = %s and data_dt = %s 
                    """
            values1 = (process_name, data_dt)
            cusor.execute(check, values1)
            if len(cusor.fetchall()) == 0:
                insert = """
                        INSERT INTO cntl.cntl_cfg_log
                        (prcs_nm, data_dt, start_dt, end_dt, status, message, source_row, target_row)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """
                values2 = (process_name, data_dt, start_dt, end_dt, status, message, source_row, target_row)
                cusor.execute(insert, values2)
                conn.commit() 
            else:
                query = """
                    UPDATE cntl.cntl_cfg_log
                    SET start_dt = %s, end_dt = %s, status = %s, message = %s, source_row=%s, target_row=%s
                    where prcs_nm = %s and data_dt = %s
                    """
                values = (start_dt, end_dt, 1, message, source_row, target_row, process_name, data_dt)
                cusor.execute(query, values)
                conn.commit() 

        def UpdateLogProcess(process_name, data_dt, start_dt, end_dt, status, message='', source_row=0, target_row=0):
            conn = Framework.Utility.GetConnection()
            cusor = conn.cursor() 
            query = """
                    UPDATE cntl.cntl_cfg_log
                    SET start_dt = %s, end_dt = %s, status = %s, message = %s, source_row=%s, target_row=%s
                    where prcs_nm = %s and data_dt = %s
                    """
            values = (start_dt, end_dt, status, message, source_row, target_row, process_name, data_dt)
            cusor.execute(query, values)
            conn.commit() 


        @classmethod
        def GetContainerId(self): 
            container_id = subprocess.check_output(
                "docker ps -q --filter 'name=jupyter_notebook'", 
                shell=True
            ).decode('utf-8').strip()  
            return container_id
 
            

        
             
 