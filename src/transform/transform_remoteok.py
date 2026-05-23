import json
from datetime import datetime
from utils.logger import get_logger

logger = get_logger("transform_remoteok")

with open("src/utils/location_mapping.json") as f:
  LOCATION_MAPPING = json.load(f)

with open("src/utils/tag_rules.json") as f:
  TAG_RULES = json.load(f)

def load_snapshot(path):
  # Load Json snapshot from disk
  try:
    with open(path, "r", encoding="utf-8") as f:
      data = json.load(f)

    jobs = data["data"][1:]
    extracted_at = data.get("extracted_at")

  except FileNotFoundError:
    logger.error(f"File not found {path}")
    jobs = []
  except json.JSONDecodeError:
    logger.error("Inavlid JSON format")
    jobs = []

  return jobs, extracted_at


def clean_jobs(jobs, extracted_at):
  # Basic cleaning of raw job records

  cleaned = []

  for job in jobs:

    sal_min = job.get("salary_min") or None
    sal_max = job.get("salary_max") or None

    if sal_min and sal_max and sal_min > sal_max:
      sal_min, sal_max = None, None

    cleaned_job = {
      "job_id": job.get("id"),
      "source": "remoteok",
      "date": job.get("date"),
      "company": (job.get("company") or "").strip(),
      "position": (job.get("position") or "").strip(),
      "tags": job.get("tags") or [],
      "location": (job.get("location") or "").strip(),
      "salary_min": sal_min,
      "salary_max": sal_max,
      "modality": "remote",
      "extracted_at": extracted_at
    }

    cleaned.append(cleaned_job)
  
  return cleaned


EXPERIENCE_MAP = {
  "jr": "junior",
  "junior": "junior", 
  "senior": "senior", 
  "sr": "senior", 
  "mid": "mid",
  "lead": "senior"}

WORLDWIDE_KEYWORDS = {"remote", "anywhere", "worldwide", "global"}

REMOTE_PREFIXES = ["remote - ", "remote – ", "remote — "]

def parse_location(job):
  # Standardize locations values

  raw_loc = (job.get("location") or "").strip().lower()

  for prefix in REMOTE_PREFIXES:
    if raw_loc. startswith(prefix):
      raw_loc = raw_loc.replace(prefix, "").strip()
      break

    # Default
  city = None

  # empty --> Unknown
  if raw_loc == "":
    job["location_name"] = "Unknown"
    job["country"] = "Unknown"
    job["city"] = city
    return job
  
  # Worldwide keywords

  if raw_loc in WORLDWIDE_KEYWORDS:
    job["location_name"] = raw_loc.title()
    job["country"] = "Worldwide"
    job["city"] = city
    return job
  
  clean_loc = raw_loc
  for kw in WORLDWIDE_KEYWORDS:
    clean_loc = clean_loc.replace(kw, "")
  clean_loc = clean_loc.strip("-,/")

  if clean_loc == "":
    job["location_name"] = raw_loc.title()
    job["country"] = "Worldwide"
    job["city"] = city
    return job


  # ---- Split ----
  if "," in raw_loc:
    parts = [p.strip() for p in clean_loc.split(",")]
    possible_country = parts[-1].strip().lower()
  else:
    possible_country = clean_loc.strip().lower()

  # Country nomalization 
  matched_country = LOCATION_MAPPING.get(possible_country)

  # ---- OUTPUT ----
  job["location_name"] = raw_loc.title()
  job["country"] = matched_country if matched_country else "Unknown"
  job["city"] = city

  return job

def enrich_location(jobs):
  for job in jobs:
    parse_location(job)

  return jobs

def normalize_company(jobs):

  for job in jobs:
    company = (job.get("company") or "").strip()

    if not company:
      company = "Unknown"
    else: 
      company = company.title()

    job["company"] = company

  return jobs

def classify_tags(jobs):
  # Classify tags into categories
  for job in jobs: 

    new_tags = []

    for tag in job.get("tags", []):
      
      tag_clean = tag.lower()

      category = "other"
      for cat, values in TAG_RULES.items():
        if tag_clean in values:
          category = cat
          break

      new_tags.append({
        "tag": tag_clean,
        "category": category
      })

    job["tags"] = new_tags

  return jobs

def normalize_experience(jobs):
  for job in jobs:

    experience = "unknown"
    job_title = (job.get("position") or "").strip().lower()

    for word in TAG_RULES["seniority"]:
      if word in job_title:
        experience = EXPERIENCE_MAP.get(word, "unknown")
        break
    
    if experience == "unknown":
      for tag in job.get("tags", []):
        if tag["category"] == "seniority":
          experience = EXPERIENCE_MAP.get(tag["tag"], "unknown")
          break
     
    job["experience"] = experience
  
  return jobs

def normalize_salary(jobs):
  for job in jobs:

    min_sal = job.get("salary_min")
    max_sal = job.get("salary_max")

    # For salary min
    if not min_sal or min_sal == 0:
      job["salary_min"] = None
    # Hourly
    elif min_sal and min_sal < 200:
      job["salary_min"] = None
    # Monthly
    elif min_sal and 300 <= min_sal <= 20000:
      job["salary_min"] = min_sal * 12
    else:
      job["salary_min"] = min_sal

    # For salary max
    if not max_sal or max_sal == 0:
      job["salary_max"] = None
    elif max_sal and max_sal < 200:
      job["salary_max"] = None
    elif max_sal and 1000 <= max_sal <= 20000:
      job["salary_max"] = max_sal * 12
    else:
      job["salary_max"] = max_sal

    if job["salary_min"] and job["salary_max"]:
      if job["salary_min"] > job["salary_max"]:
        job["salary_min"] = None
        job["salary_max"] = None

  return jobs

def normlize_date(jobs):

  for job in jobs:
    raw_date = job.get("date")
    try:
      dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
      job["full_date"] = dt.date()
      job["day"] = dt.day
      job["month"] = dt.month
      job["year"] = dt.year
    except Exception:
      job["full_date"] = None
      job["day"] = None
      job["month"] = None
      job["year"] = None
      logger.warning(f"Warning: invalid date in job {job.get('job_id')} -- {raw_date}")

  return jobs

def transform_remoteok(path):

  jobs, extracted_at = load_snapshot(path)
  jobs = clean_jobs(jobs, extracted_at)
  jobs = enrich_location(jobs)
  jobs = normalize_company(jobs)
  jobs = classify_tags(jobs)
  jobs = normalize_experience(jobs)
  jobs = normalize_salary(jobs)
  jobs = normlize_date(jobs)

  logger.info(f"Transformation completed - Jobs processed: {len(jobs)}")

  return jobs