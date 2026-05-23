import os
import json
from datetime import datetime

def get_latest_raw_file(root_path):
  
  latest_file = None
  latest_date = None

  for root, dirs, files in os.walk(root_path):
    for file in files:
      if file.endswith(".json"):
        full_path = os.path.join(root, file)

        try:
          with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            extracted_at = data.get("extracted_at")

            if not extracted_at:
              continue

            extracted_date = datetime.fromisoformat(extracted_at)

            if latest_date is None or extracted_date > latest_date:
              latest_date = extracted_date
              latest_file = full_path

        except Exception:
          continue
  
  if not latest_file:
    raise Exception("The system did not find a valid file")
  
  return latest_file