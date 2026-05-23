import json
from collections import Counter

file_path = "data/raw/remoteok/2026/03/20260305_162406.json"

# Load Json file
with open(file_path, "r", encoding="utf-8") as f:
  data = json.load(f)

# Access the list of records
records = data["data"]

# The first record in RemoteOk is legal information, not a job
jobs = records[1:]

print(f"Total jobs in snapshot: {len(jobs)}")


#------------------------------
# Companies profiling
#------------------------------

companies = set()

for job in jobs:
  companies.add(job['company'])

print(f"Unique companies: {len(companies)}")

#------------------------------
# Location profiling
#------------------------------

locations = Counter()

for job in jobs:
  loc = job["location"].strip()

  # RemoteOk sometimes leaves location empty
  # The website interprets this a 'Worldwide'
  if loc == "":
    loc = "Worldwide"

  locations[loc] += 1

print(f"Unique locations: {len(locations)}")

print("Top 10 locations: ")
for loc, count in locations.most_common(10):
  print(loc, count)

#------------------------------
# Tag profiling
#------------------------------  

tags = Counter()

for job in jobs:
  for tag in job["tags"]:
    tags[tag.lower()] += 1

print(f"\nUnique tags: {len(tags)}")

print("\nTop 20 tags:")
for tag, count in tags.most_common(20):
  print(tag, count)


#------------------------------
# Salary profiling
#------------------------------

salary_jobs = 0
zero_salary = 0

salary_values = []

for job in jobs:
  min_salary = job["salary_min"]
  max_salary = job["salary_max"]

  if min_salary == 0 and max_salary == 0:
    zero_salary += 1
  else:
    salary_jobs += 1
    salary_values.append(min_salary)
    salary_values.append(max_salary)

print(f"\nJobs with salary information: {salary_jobs}")
print(f"Jobs without salary information: {zero_salary}")


#------------------------------
# Date profiling
#------------------------------

dates = [job["date"] for job in jobs]

print(f"\nEarliest job posting date: {min(dates)}")
print(f"Latest job postinf date: {max(dates)}")

#------------------------------
# Detect multi-location cases
#------------------------------

print("\nLocations with multiple countries:")

for loc in locations:
  if "," in loc or ";" in loc:
    print(loc)