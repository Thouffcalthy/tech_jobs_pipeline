from utils.logger import get_logger
logger = get_logger("load_bridge")

def load_bridge_job_tag(jobs, fact_job_lookup, tag_lookup, source_lookup, conn):
  cursor = conn.cursor()

  rows_inserted = 0
  rows_skipped = 0

  for job in jobs:
    source_key = source_lookup.get(job["source"])
    fact_job_key = fact_job_lookup.get((job["job_id"], source_key))

    if fact_job_key is None:
      rows_skipped += 1
      continue

    for tag in job.get("tags", []):
      tag_key = tag_lookup.get((tag["tag"], source_key))

      if tag_key is None:
        continue

      cursor.execute("""
                     INSERT INTO bridge_job_tag (fact_job_key, tag_key)
                     VALUES (%s, %s)
                     ON CONFLICT (fact_job_key, tag_key) DO NOTHING
                     """, (fact_job_key, tag_key))
      rows_inserted += 1

  cursor.close()

  logger.info(f"Bridge rows inserted: {rows_inserted}")

  if rows_skipped > 0:
    logger.warning(f"Bridge loaded - rows inserted: {rows_inserted}, skipped: {rows_skipped}")
  else:
    logger.info(f"Bridge loaded - rows inserted: {rows_inserted}, skipped: {rows_skipped}")

    