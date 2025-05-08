import os, sys
import psycopg2
import shutil

# str(sys.argv[0]) # file name

def get_folder_detail(stream_name):
    conn = psycopg2.connect(
        host="localhost",     
        port=5432,            
        database="airflow",   
        user="airflow",       
        password="airflow"  
    )
    cusor = conn.cursor() 
    check = """
            select prcs.prcs_nm 
            from cntl.cntl_cfg_strem strem
            left join cntl.cntl_cfg_prcs_grp prcs_grp
                on strem.strem_nm  = prcs_grp.strem_nm 
            left join cntl.cntl_cfg_prcs prcs
                on prcs_grp.prcs_grp = prcs.prcs_grp 
            where strem.strem_nm = %s 
            """
    values1 = (stream_name, )
    cusor.execute(check, values1)

    return [_[0] for _ in cusor.fetchall()]

def create_nested_folder():
    template_path = '../../TEMPLATE'
    list_of_process = get_folder_detail(stream_name)

    root_path = f'../../dags/script/{folder_name}'
    os.makedirs(root_path)

    stream_path = f'../../dags/script/{folder_name}/01_stream'
    os.makedirs(stream_path)
    shutil.copy(template_path + '/stream_template.py', stream_path + f'/{stream_name}.py')


    process_path = f'../../dags/script/{folder_name}/02_process'
    os.makedirs(process_path)
    for process in list_of_process:
        shutil.copy(template_path + '/process_template.py', process_path + f'/{process}.py')


def main():
    create_nested_folder()


if __name__ == "__main__":
    folder_name = str(sys.argv[1]) 
    stream_name = str(sys.argv[2])
    main()
