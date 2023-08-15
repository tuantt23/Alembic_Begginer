from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker

#connection string format: driver+postgresql://user:pass@host:port/DBname
url = URL.create(drivername="postgresql+psycopg2",
          username="testuser",
          password="testpassword",
          host="localhost",
          port=5432,
          database="testDB",
          )
engine = create_engine(url,echo=True)
session_pool = sessionmaker(engine)
#get a session from session pool

#Option 2
with session_pool() as session:
    query = text("""
    SELECT * FROM users;
    """)
    result = session.execute(query)
    print(result)
    for row in result:
        print(row)

    # and commit the changes
    #session.commit()
    # session.close()

    #Option1 
# session = session_pool()
# session.execute()
# session.commit()
# session.close()