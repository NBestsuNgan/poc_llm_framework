INSERT INTO cntl.cntl_cfg_strem
(strem_nm, question, upt_dt, act_f, strem_owner)
VALUES('Brids_strem', 'describe the characteristic of the brid from the follow context', CURRENT_TIMESTAMP, 1, 'Animalstupid');
INSERT INTO cntl.cntl_cfg_strem
(strem_nm, question, upt_dt, act_f, strem_owner)
VALUES('testrun', 'how are you today?', CURRENT_TIMESTAMP, 1, 'Animalstupid');


INSERT INTO cntl.cntl_cfg_prcs_grp
(prcs_grp, strem_nm, prir, act_f, upt_dt)
VALUES('BridsGrp', 'Brids_strem', 1, 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs_grp
(prcs_grp, strem_nm, prir, act_f, upt_dt)
VALUES('BridsGrp2', 'Brids_strem', 1, 0, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs_grp
(prcs_grp, strem_nm, prir, act_f, upt_dt)
VALUES('testrunGrp', 'testrun', 1, 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs_grp
(prcs_grp, strem_nm, prir, act_f, upt_dt)
VALUES('testrunGrp2', 'testrun', 1, 1, CURRENT_TIMESTAMP);


INSERT INTO cntl.cntl_cfg_prcs
(prcs_nm, prcs_grp, prir, sys_file, embed_model, gen_model, collection, nb_path_nm, nb_parm, act_f, upt_dt)
VALUES('Docbirdpdf', 'BridsGrp', 1, 'bridpdf', 'mxbai-embed-large', 'deepseek-r1:7b', 'Bridknowledge', 'Ingest/silo2vector.ipynb', 'datalake|raw/pdf|Birddiversityanddistribution', 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs
(prcs_nm, prcs_grp, prir, sys_file, embed_model, gen_model, collection, nb_path_nm, nb_parm, act_f, upt_dt)
VALUES('Docbirdcsv', 'BridsGrp', 1, 'bridcsv', 'mxbai-embed-large', 'deepseek-r1:7b', 'Bridknowledge', 'Ingest/silo2vector.ipynb', 'datalake|raw/text-csv|PFW_spp_translation_table_May2024', 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs
(prcs_nm, prcs_grp, prir, sys_file, embed_model, gen_model, collection, nb_path_nm, nb_parm, act_f, upt_dt)
VALUES('Llmbird', 'BridsGrp', 2, '', 'mxbai-embed-large', 'deepseek-r1:7b', 'Bridknowledge', 'Arag/Adaptiverag.ipynb', 'llmnok', 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs
(prcs_nm, prcs_grp, prir, sys_file, embed_model, gen_model, collection, nb_path_nm, nb_parm, act_f, upt_dt)
VALUES('testrun1', 'testrunGrp', 1, '', 'mxbai-embed-large', 'deepseek-r1:7b', 'Bridknowledge', 'test_run/test_run.ipynb', 'testrun1', 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs
(prcs_nm, prcs_grp, prir, sys_file, embed_model, gen_model, collection, nb_path_nm, nb_parm, act_f, upt_dt)
VALUES('testrun2', 'testrunGrp', 2, '', 'mxbai-embed-large', 'deepseek-r1:7b', 'Bridknowledge', 'test_run/test_run.ipynb', 'testrun2', 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs
(prcs_nm, prcs_grp, prir, sys_file, embed_model, gen_model, collection, nb_path_nm, nb_parm, act_f, upt_dt)
VALUES('testrun3', 'testrunGrp2', 1, '', 'mxbai-embed-large', 'deepseek-r1:7b', 'Bridknowledge', 'test_run/test_run.ipynb', 'testrun3', 1, CURRENT_TIMESTAMP);


INSERT INTO cntl.cntl_sys_fle
(sys_nm, file_type, dlm, chunk_size, overlap, upt_dt)
VALUES('bridpdf', 'pdf', '', 300, 50, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_sys_fle
(sys_nm, file_type, dlm, chunk_size, overlap, upt_dt)
VALUES('bridtxt', 'txt', ',', 300, 50, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_sys_fle
(sys_nm, file_type, dlm, chunk_size, overlap, upt_dt)
VALUES('bridcsv', 'csv', ',', 300, 50, CURRENT_TIMESTAMP);


INSERT INTO cntl.cntl_cfg_prcs_depn
(prcs_nm, dpnd_prcs_nm, act_f, upt_dt)
VALUES('Llmbird', 'Docbirdpdf', 1, CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_prcs_depn
(prcs_nm, dpnd_prcs_nm, act_f, upt_dt)
VALUES('Llmbird', 'Docbirdcsv', 1, CURRENT_TIMESTAMP);


INSERT INTO cntl.cntl_cfg_schedule
(strem_nm, minutes, hours, day_month, months, day_week, upt_dt)
VALUES('Brids_strem', '0', '13', '*', '*', '*', CURRENT_TIMESTAMP);
INSERT INTO cntl.cntl_cfg_schedule
(strem_nm, minutes, hours, day_month, months, day_week, upt_dt)
VALUES('testrun', '0', '20', '*', '*', '*', CURRENT_TIMESTAMP);