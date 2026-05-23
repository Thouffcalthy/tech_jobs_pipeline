from utils.db_connection import get_connection

def load_dim_company(dim_company, conn):
  cursor = conn.cursor()

  for row in dim_company:
    cursor.execute("""
                INSERT INTO dim_company (company_name)
                VALUES (%s)
                ON CONFLICT (company_name) DO NOTHING
                """, (row["company_name"],))
    
  conn.commit()
  cursor.close()

def get_company_lookup(conn):
  cursor = conn.cursor()

  cursor.execute("""
                 SELECT company_key, company_name
                 FROM dim_company
                 """)
  
  rows = cursor.fetchall()

  lookup = {name: key for key, name in rows}

  cursor.close()
  return lookup

def load_dim_date(dim_date, conn):
  cursor = conn.cursor()

  for row in dim_date:
    cursor.execute("""
                    INSERT INTO dim_date (full_date, day, month, year)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (full_date) DO NOTHING
                   """, (row["full_date"], row["day"], row["month"], row["year"],))
    
  conn.commit()
  cursor.close()

def get_date_lookup(conn):
  cursor = conn.cursor()

  cursor.execute("""
                 SELECT date_key, full_date
                 FROM dim_date
                 """)
  
  rows = cursor.fetchall()
  lookup = {date: key for key, date in rows}

  cursor.close()
  return lookup

def load_dim_location(dim_location, conn):
  cursor = conn.cursor()

  for row in dim_location:
    cursor.execute("""
                  INSERT INTO dim_location (location_name, country, city)
                  VALUES (%s, %s, %s)
                  ON CONFLICT (location_name) DO NOTHING;
                  """, (row["location_name"], row["country"], row["city"]))

  conn.commit()  
  cursor.close()

def get_location_lookup(conn):
  cursor = conn.cursor()

  cursor.execute("""
                 SELECT location_key, location_name
                 FROM dim_location
                 """)
  
  rows = cursor.fetchall()

  lookup = {loc: key for key, loc in rows}

  cursor.close()
  return lookup

def load_dim_source(dim_source, conn):
  cursor = conn.cursor()

  for row in dim_source:

    cursor.execute("""
                   INSERT INTO dim_source (name)
                   VALUES (%s)
                   ON CONFLICT (name) DO NOTHING
                   """, (row["name"],))
    
  conn.commit()  
  cursor.close()

def get_source_lookup(conn):
  cursor = conn.cursor()

  cursor.execute("""
                 SELECT source_key, name
                 FROM dim_source
                 """)

  rows = cursor.fetchall()
  lookup = {source: key for key, source in rows}

  cursor.close()
  return lookup

def load_dim_experience(dim_experience, conn):
  cursor = conn.cursor()
  
  for row in dim_experience:
    cursor.execute("""
                  INSERT INTO dim_experience (experience)
                  VALUES (%s)
                  ON CONFLICT (experience) DO NOTHING
                  """, (row["experience"],))
    
  conn.commit()  
  cursor.close()

def get_experience_lookup(conn):
  cursor = conn.cursor()

  cursor.execute("""
                 SELECT experience_key, experience
                 FROM dim_experience
                 """)

  rows = cursor.fetchall()
  lookup = {exp: key for key, exp in rows}

  cursor.close()
  return lookup  

def load_dim_modality(dim_modality, conn):
  cursor = conn.cursor()

  for raw in dim_modality:

    cursor.execute("""
                   INSERT INTO dim_modality (modality)
                   VALUES (%s)
                   ON CONFLICT (modality) DO NOTHING
                   """, (raw["modality"],))

  conn.commit()  
  cursor.close()

def get_modality_lookup(conn):
  cursor = conn.cursor()

  cursor.execute("""
                 SELECT modality_key, modality
                 FROM dim_modality
                 """)
  
  rows = cursor.fetchall()
  lookup = {modality: key for key, modality in rows}

  cursor.close()
  return lookup

def load_dim_tag(dim_tag, source_lookup, conn):
  cursor = conn.cursor()

  for row in dim_tag:

    source_key = source_lookup.get(row["source"])

    if source_key is None:
      print(f"Unknown source: {row['source']}")
      continue

    cursor.execute("""INSERT INTO dim_tag (tag_name, source_key, tag_category)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (source_key, tag_name) DO NOTHING
                   """, (row["tag_name"], source_key, row["category"]))
    
  conn.commit()
  cursor.close()

def get_tag_lookup(conn):
  cursor = conn.cursor()

  cursor.execute("""
                 SELECT tag_key, tag_name, source_key
                 FROM dim_tag
                 """)
  
  rows = cursor.fetchall()
  lookup = {(tag_name, source): key for key, tag_name, source in rows}

  cursor.close()
  return lookup


