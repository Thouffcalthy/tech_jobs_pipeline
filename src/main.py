import os
from extract.remoteok_extractor import extract_remoteok
from transform.transform_remoteok import transform_remoteok

from utils.get_latest_raw_file import get_latest_raw_file
from utils.db_connection import get_connection
from utils.logger import get_logger

from model.build_dimensions import (
  build_dim_company,
  build_dim_location,
  build_dim_source,
  build_dim_modality,
  build_dim_experience,
  build_dim_date,
  build_dim_tag
)
from load.load_dimensions import (
  load_dim_company, get_company_lookup,
  load_dim_date, get_date_lookup,
  load_dim_location, get_location_lookup,
  load_dim_source, get_source_lookup,
  load_dim_experience, get_experience_lookup,
  load_dim_modality, get_modality_lookup,
  load_dim_tag, get_tag_lookup
)

from load.load_fact_table import (load_fact_table, get_fact_job_lookup)
from load.load_bridge import load_bridge_job_tag

logger = get_logger("main")

def main():

  try: 
    # 1. EXTRACT

    extract_remoteok()

    root_path = "data/raw/remoteok/"
    raw_path  = get_latest_raw_file(root_path)
    path = os.path.normpath(raw_path)
    print(f"raw data: {path}")

    #path = "data/raw/remoteok/2026/05/20260521_112514.json"
  except Exception as e:
    logger.error(f"Extract failed: {e}")
    return
  
  conn = None

  try:
    conn = get_connection()
    logger.info("Pipeline started")

    # 2. TRANSFORM
    jobs = transform_remoteok(path)
    logger.info(f"Transform completed - jobs processed: {len(jobs)}")

    # 3. BUILD DIMENSIONS
    dim_company = build_dim_company(jobs)
    dim_location = build_dim_location(jobs)
    dim_source = build_dim_source(jobs)
    dim_modality = build_dim_modality(jobs)
    dim_experience = build_dim_experience(jobs)
    dim_date = build_dim_date(jobs)
    dim_tag = build_dim_tag(jobs)

    logger.info(f"Dimensions built - companies: {len(dim_company)}, locations: {len(dim_location)},  sources: {len(dim_source)}, tags: {len(dim_tag)}")

    # 4. LOAD DIMENSIONS
    load_dim_source(dim_source, conn)
    source_lookup = get_source_lookup(conn)
    load_dim_company(dim_company, conn)
    load_dim_location(dim_location, conn)
    load_dim_modality(dim_modality, conn)
    load_dim_experience(dim_experience, conn)
    load_dim_date(dim_date, conn)
    load_dim_tag(dim_tag, source_lookup, conn)

    logger.info("Dimensions loaded")

    # 5. LOAD FACT_JOBS
    date_lookup = get_date_lookup(conn)
    company_lookup = get_company_lookup(conn)
    location_lookup = get_location_lookup(conn)
    source_lookup = get_source_lookup(conn)
    experience_lookup = get_experience_lookup(conn)
    modality_lookup = get_modality_lookup(conn)

    assert "Unknown" in location_lookup, "Missing 'Unknown' in dim_location"
    
    load_fact_table(
      jobs,
      date_lookup,
      company_lookup,
      location_lookup,
      source_lookup,
      experience_lookup,
      modality_lookup,
      conn
    )

    logger.info("Fact table loaded")

    # 6. LOAD BRIDGE_TABLE
    fact_job_lookup = get_fact_job_lookup(conn)
    tag_lookup = get_tag_lookup(conn)
    load_bridge_job_tag(jobs, fact_job_lookup, tag_lookup, source_lookup, conn)

    conn.commit()
    logger.info("Pipeline completed successfully")

  except Exception as e:
    if conn:
      conn.rollback()
    logger.error(f"Pipeline failed, rollback executed: {e}")
  
  finally:
    if conn:
      conn.close()
    logger.info("Connection closed")

if __name__=="__main__":
  main()