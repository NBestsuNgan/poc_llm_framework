CREATE TABLE cntl.cntl_cfg_strem (
	strem_nm varchar NOT NULL,
	question varchar NOT NULL,
	upt_dt timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	act_f int4 NULL,
	strem_owner varchar NULL,
	CONSTRAINT cntl_cfg_strem_pkey PRIMARY KEY (strem_nm)
);


CREATE TABLE cntl.cntl_cfg_prcs_grp (
	prcs_grp varchar NOT NULL,
	strem_nm varchar NOT NULL,
	prir int4 NOT NULL,
	act_f int4 NOT NULL,
	upt_dt timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT cntl_cfg_prcs_grp_pkey PRIMARY KEY (prcs_grp)
);


CREATE TABLE cntl.cntl_cfg_prcs (
	prcs_nm varchar NOT NULL,
	prcs_grp varchar NOT NULL,
	prir int4 NOT NULL,
	sys_file varchar NULL,
	embed_model varchar NULL,
	gen_model varchar NULL,
	collection varchar NULL,
	nb_path_nm varchar NULL,
	nb_parm varchar NULL,
	act_f int4 NOT NULL,
	upt_dt timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT cntl_cfg_prcs_pkey PRIMARY KEY (prcs_nm)
);


CREATE TABLE cntl.cntl_cfg_prcs_depn (
	prcs_nm varchar NOT NULL,
	dpnd_prcs_nm varchar NOT NULL,
	act_f int4 NOT NULL,
	upt_dt timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT cntl_cfg_prcs_depn_pkey PRIMARY KEY (prcs_nm, dpnd_prcs_nm)
);


CREATE TABLE cntl.cntl_sys_fle (
	sys_nm varchar NOT NULL,
	file_type varchar NOT NULL,
	dlm varchar NULL,
	chunk_size int4 NULL,
	overlap int4 NULL,
	upt_dt timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT cntl_sys_fle_pkey PRIMARY KEY (sys_nm)
);

CREATE TABLE cntl.cntl_cfg_schedule (
	strem_nm varchar NOT NULL,
	minutes varchar NOT NULL,
	hours varchar NOT NULL,
	day_month varchar NOT NULL,
	months varchar NOT NULL,
	day_week varchar NULL,
	upt_dt timestamp NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cntl.cntl_cfg_log (
	prcs_nm varchar NOT NULL,
	data_dt timestamp NULL,
	start_dt timestamp NOT NULL,
	end_dt timestamp NOT NULL,
	status int4 NOT NULL,
	message text NULL,
	source_row int4 NULL,
	target_row int4 NULL
);