CREATE TABLE dim_date (
	date_key INT GENERATED ALWAYS AS IDENTITY,
	full_date DATE NOT NULL UNIQUE,
	day INT,
	month INT,
	year INT,
	CONSTRAINT pk_date PRIMARY KEY (date_key),
	CONSTRAINT ck_month CHECK (month BETWEEN 1 AND 12),
	CONSTRAINT ck_day CHECK (day BETWEEN 1 AND 31) 
);

CREATE TABLE dim_company (
	company_key INT GENERATED ALWAYS AS IDENTITY,
	company_name VARCHAR(100) UNIQUE NOT NULL,
	CONSTRAINT pk_company PRIMARY KEY (company_key)
);

CREATE TABLE dim_location (
	location_key INT GENERATED ALWAYS AS IDENTITY,
	location_name VARCHAR(100) NOT NULL,
	country VARCHAR(50),
	city VARCHAR(50),
	CONSTRAINT pk_location PRIMARY KEY (location_key),
	CONSTRAINT uq_location UNIQUE (location_name)
);

CREATE TABLE dim_source (
	source_key INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(30) UNIQUE NOT NULL,
	CONSTRAINT pk_source PRIMARY KEY (source_key)
);

CREATE TYPE exp_experience AS ENUM ('junior', 'mid', 'senior', 'unknown');

CREATE TABLE dim_experience (
	experience_key INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	experience exp_experience NOT NULL UNIQUE
);


CREATE TYPE mod_mode AS ENUM ('onsite', 'hybrid', 'remote', 'unknown');

CREATE TABLE dim_modality (
	modality_key INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	modality mod_mode NOT NULL UNIQUE
);

CREATE TYPE cat_tagcategory AS ENUM ('technology', 'seniority', 'rol', 'domain', 'work_type', 'other');

CREATE TABLE dim_tag (
	tag_key INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	tag_name VARCHAR(50) NOT NULL,
	source_key INT NOT NULL,
	tag_category cat_tagcategory NOT NULL,

	CONSTRAINT fk_dim_source 
		FOREIGN KEY (source_key)
		REFERENCES dim_source(source_key),
	
	CONSTRAINT uq_tag UNIQUE (source_key, tag_name)
);

CREATE TABLE fact_jobs (
	fact_job_key INT GENERATED ALWAYS AS IDENTITY,
	fact_job_title VARCHAR(100),
	api_job_id VARCHAR(100) NOT NULL,
	date_key INT NOT NULL,
	company_key INT NOT NULL,
	location_key INT NOT NULL,
	source_key INT NOT NULL,
	experience_key INT NOT NULL,
	modality_key INT NOT NULL,
	salary_min_usd NUMERIC(10,2),
	salary_max_usd NUMERIC(10,2),
	is_active BOOLEAN DEFAULT TRUE,
	last_seen TIMESTAMP,
	extracted_at TIMESTAMP,
	CONSTRAINT pk_fact_jobs PRIMARY KEY (fact_job_key),
	CONSTRAINT uq_job_source UNIQUE (api_job_id, source_key),
	CONSTRAINT fk_dim_date 
		FOREIGN KEY (date_key)
		REFERENCES dim_date (date_key),
	CONSTRAINT fk_dim_company
		FOREIGN KEY (company_key)
		REFERENCES dim_company (company_key),
	CONSTRAINT fk_dim_location
		FOREIGN KEY (location_key)
		REFERENCES dim_location (location_key),
	CONSTRAINT fk_dim_source
		FOREIGN KEY (source_key)
		REFERENCES dim_source (source_key),
	CONSTRAINT fk_dim_modality 
		FOREIGN KEY (modality_key)
		REFERENCES dim_modality (modality_key),
	CONSTRAINT fk_dim_experience
		FOREIGN KEY (experience_key)
		REFERENCES dim_experience (experience_key),
	CONSTRAINT chk_salary_range
		CHECK (
			salary_min_usd IS NULL
			OR salary_max_usd IS NULL
			OR salary_min_usd <= salary_max_usd
		)
);


CREATE TABLE bridge_job_tag (
	fact_job_key INT NOT NULL,
	tag_key INT NOT NULL,
	CONSTRAINT pk_jobs_tag PRIMARY KEY (fact_job_key,tag_key),
	CONSTRAINT fk_fact_jobs
		FOREIGN KEY (fact_job_key)
		REFERENCES fact_jobs (fact_job_key)
		ON DELETE CASCADE,
	CONSTRAINT fk_dim_tag
		FOREIGN KEY (tag_key)
		REFERENCES dim_tag (tag_key)
);
