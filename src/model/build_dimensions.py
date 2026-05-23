def build_dim_company(jobs):

  companies = set()

  for job in jobs:
    company = job.get("company")

    if company and company.strip():
      companies.add(company.strip())

  dim_company = [
    {"company_name": c}
    for c in companies
  ]

  return dim_company

def build_dim_location(jobs):

  locations = set()

  for job in jobs:
    location_name = job.get("location_name")
    country = job.get("country")

    if location_name:
      locations.add((location_name.strip(), country))

  dim_location = [
    {
      "location_name": loc,
      "country": country,
      "city": None
    }
    for loc, country in locations
  ]

  return dim_location

def build_dim_source(jobs):

  sources = set()

  for job in jobs:

    source = job.get("source")
    
    if source and source.strip():
      sources.add(source)

  dim_source = [
    {
      "name": s
    }
    for s in sources
  ]

  return dim_source

def build_dim_modality(jobs):

  modalities = set()

  for job in jobs:

    modality = job.get("modality")

    if modality:
      modalities.add(modality)

  dim_modality = [
    {
      "modality": mod
    }
    for mod in modalities
  ]

  return dim_modality

def build_dim_experience(jobs):
  experience_items = set()

  for job in jobs:
    exp = job.get("experience")

    if exp:
      experience_items.add(exp)

  dim_experience = [
    {
      "experience": e
    }
    for e in experience_items
  ]

  return dim_experience

def build_dim_date(jobs):

  dates = set()

  for job in jobs:
    full_date = job.get("full_date")

    if full_date:
      dates.add(full_date)

  dim_date = []

  for d in dates:
    dim_date.append({
      "full_date": d,
      "day": d.day,
      "month": d.month,
      "year": d.year
    })

  return dim_date

def build_dim_tag(jobs):

  tag_map = {}

  for job in jobs:

    source = job.get("source")

    for tag in job.get("tags", []):

      tag_name = tag.get("tag")
      category = tag.get("category")

      if not tag_name or not source:
        continue

      key = (source, tag_name)

      if key not in tag_map:
        tag_map[key] = category

  dim_tag = [
    {
      "tag_name": k[1],
      "source": k[0],
      "category": v
    }
    for k, v in tag_map.items()
  ]

  return dim_tag