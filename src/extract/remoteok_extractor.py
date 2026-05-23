import requests
import json
from datetime import datetime
from pathlib import Path
from utils.logger import get_logger

logger = get_logger("remoteok_extractor")

url = "https://remoteok.com/api"

base_dir = Path(__file__).resolve().parents[2]


def extract_remoteok():
  logger.info("Extract started - calling RemoteOK API")

  headers = {
    "User_Agent" : "tech_jobs_data_pipeline"
  }

  response = requests.get(url, headers=headers, timeout=30)

  if response.status_code != 200:
    logger.error(f"API error: {response.status_code}")
    raise Exception(f"API error: {response.status_code}")

  try: 
    data = response.json()
  except Exception:
    logger.error("Invalid JSON response")
    raise Exception("Invalid JSON response")

  if not isinstance(data, list):
    logger.error("Unexpected API structure")
    raise Exception("Unexpected API structure")

  timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

  output = {
    "source" : "remoteok",
    "endpoint": url,
    "extracted_at": datetime.utcnow().isoformat(),
    "record_count": len(data),
    "data": data
  }

  now = datetime.utcnow()

  year = now.strftime("%Y")
  month = now.strftime("%m")

  raw_path = base_dir/"data"/"raw"/"remoteok/"/year/month
  raw_path.mkdir(parents=True, exist_ok=True)

  file_path = raw_path / f"{timestamp}.json"

  with open(file_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

  logger.info(f"Saved {len(data)} records to {file_path}")