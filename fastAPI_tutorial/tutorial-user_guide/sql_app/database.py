"""Create the SQLAlchemy parts"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Tip
    # This is the main line that you would have to modify
    # if you wanted to use a different database.
    
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# The file will be located at the same directory in the file `sql_app.db`.
    # That's why the last part is `./sql_app.db`.

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        
        connect_args={"check_same_thread": False}
        # ...is needed only for SQLite. It's NOT NEEDED FOR OTHER DATABASES.
        
        # Technical Details
            # By default SQLite will 
                # ONLY ALLOW ONE THREAD TO COMMUNICATE WITH IT, 
                    # assuming that each thread would handle an independent request.
                # This is to prevent accidentally sharing the same connection for different things 
                    # (for different requests).
                # But in FastAPI, using normal functions (def) 
                    # MORE THAN ONE THREAD COULD INTERACT WITH THE DATABASE FOR THE SAME REQUEST, 
                    # so we need to make SQLite know that it should allow that with
                        # `connect_args={"check_same_thread": False}`.
                    # Also, we will make sure each request 
                        # gets its own database connection session in a dependency, 
                           # so there's no need for that default mechanism.
            )

# Create a `SessionLocal` class. 
# The class itself is NOT a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# once we create an instance of the SessionLocal class, 
# this instance will be the actual database session.

# Create a `Base` class. 
Base = declarative_base()
# Later we will inherit from this class to 
    # create each of the database models or classes (the ORM models)
