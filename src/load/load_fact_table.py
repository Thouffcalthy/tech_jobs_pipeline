from utils.db_connection import get_connection
from utils.logger import get_logger

logger = get_logger("load_fact_table")

def load_fact_table(
    jobs,
    date_lookup,
    company_lookup,
    location_lookup,
    source_lookup, 
    experience_lookup,
    modality_lookup,
    conn
    ):
  
  cursor = conn.cursor()

  jobs_skipped = 0

  source_key = source_lookup.get(jobs[0]["source"])
  cursor.execute("""
                 UPDATE fact_jobs 
                 SET is_active = FALSE
                 WHERE source_key = %s;
                 """, (source_key,))

  for job in jobs:

    date_key = date_lookup.get(job["full_date"])
    company_key = company_lookup.get(job["company"])
    location_key = location_lookup.get(job["location_name"])
    
    if location_key is None:
      location_key = location_lookup.get("Unknown")
      
    source_key = source_lookup.get(job["source"])
    experience_key = experience_lookup.get(job["experience"])
    modality_key = modality_lookup.get(job["modality"])

    # Skipped jobs
    missing = []

    if date_key is None:
      missing.append("date")
    if company_key is None:
      missing.append("company")
    if location_key is None:
      missing.append("location")
    if source_key is None:
      missing.append("source")
    if experience_key is None:
      missing.append("experience")
    if modality_key is None:
      missing.append("modality")
    if missing:
      logger.warning(f"Skipping job {job['job_id']} due to missing: {missing}")
      logger.warning(f"Debug --> location: {job.get('location_name')}, company: {job.get('company')}")
      jobs_skipped += 1
      continue

    cursor.execute("""
                   INSERT INTO fact_jobs (fact_job_title, api_job_id, date_key, company_key,
                                          location_key, source_key, experience_key, modality_key,
                                          salary_min_usd, salary_max_usd, last_seen, extracted_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
                   ON CONFLICT (api_job_id, source_key) DO UPDATE SET
                    is_active = TRUE,
                    last_seen = CURRENT_TIMESTAMP
                   """, (job["position"], job["job_id"], date_key, company_key,
                        location_key, source_key, experience_key, modality_key,
                         job["salary_min"], job["salary_max"], job["extracted_at"]))
  
  if jobs_skipped > 0:
    logger.warning(f"Fact table loaded - Jobs skipped: {jobs_skipped}")
  else: 
    logger.info(f"Fact table loaded - Jobs skipped: {jobs_skipped}")  
    
  cursor.close()


def get_fact_job_lookup(conn):

  cursor = conn.cursor()

  cursor.execute("""
                 SELECT api_job_id, source_key, fact_job_key
                 FROM fact_jobs
                 """)
  
  rows = cursor.fetchall()
  # key = (api_job_id, source_key) in fact_job_key

  lookup = {(api_job_id, source_key): fact_job_key for api_job_id, source_key, fact_job_key in rows}

  cursor.close()
  return lookup