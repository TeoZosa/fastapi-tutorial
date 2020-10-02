"""SQL (Relational) Databases"""
# FastAPI doesn't require you to use a SQL (relational) database.
# But you can use any relational database that you want.
    # Here we'll see an example using SQLAlchemy.
        # You can easily adapt it to any database supported by SQLAlchemy, like:
            # PostgreSQL
            # MySQL
            # SQLite
            # Oracle
            # Microsoft SQL Server, 
            # etc.
    # In this example, we'll use SQLite, 
        # because it uses a single file 
        # and Python has integrated support. 
        # So, you can copy this example and run it as is.
    # Later, for your production application, 
        # you might want to use a database server like PostgreSQL.

# Tip
    # There is an official project generator with 
        # FastAPI and PostgreSQL, 
        # all based on Docker, 
        # including a frontend and more tools: 
            # https://github.com/tiangolo/full-stack-fastapi-postgresql

# Note
    # most of the code is the standard SQLAlchemy code you would use with any framework.
    # The FastAPI specific code is as small as always.

## ORMs
# FastAPI works with 
    # any database and 
    # any style of library to talk to the database.
# A common pattern is to use an 
    # "ORM": an "object-relational mapping" library.
# An ORM has tools to convert ("map") between objects in code and database tables ("relations").
# With an ORM, you normally 
    # create a class that represents a table in a SQL database, 
    # each attribute of the class represents a column, with a name and a type.
    
    # For example 
        # a class `Pet` could represent a SQL table `pets`.
        # And each instance object of that class represents a row in the database.
        # For example 
            # an object `orion_cat` (an instance of `Pet`) could have 
                # an attribute `orion_cat.type`, for the column type. 
                # And the value of that attribute could be, e.g. "cat".
            
# These ORMs also have tools to make the connections or relations between tables or entities.
    # This way, you could also have an attribute 
        # `orion_cat.owner` 
    # and the owner would contain the data for this pet's owner, 
        # taken from the table `owners`.
    # So, `orion_cat.owner.name` could be the name of this pet's owner.
        # (from the `name` column in the `owners` table) 
            # It could have a value like "Arquilian".
    # And the ORM will do all the work to get the information from the 
        # corresponding table `owners` 
        # when you try to access it from your `pet` object.

# Common ORMs are for example: 
    # Django-ORM (part of the Django framework), 
    # SQLAlchemy ORM (part of SQLAlchemy, independent of framework) and 
    # Peewee (independent of framework), 
    # among others.

# Here we will see how to work with SQLAlchemy ORM.
    # In a similar way you could use any other ORM.

# Tip
    # There's an equivalent article using Peewee in the docs.

## File structure

# For these examples, let's say you have a directory named `tutorial-user_guide` 
# that contains a sub-directory called `sql_app` with a structure like this:
    # .
    # └── sql_app
    #     ├── __init__.py
    #     ├── crud.py
    #     ├── database.py
    #     ├── main.py
    #     ├── models.py
    #     └── schemas.py
# The file __init__.py is just an empty file, 
    # but it tells Python that `sql_app` with all its modules (Python files) is a package.
# Now let's see what each file/module does.

## Create the SQLAlchemy parts
    # Let's refer to the file `sql_app/database.py`.

"""Interact with the database directly"""
# to explore the SQLite database (file) directly, independently of FastAPI, to 
    # debug its contents, 
    # add tables, columns, records, 
    # modify data, 
    # etc. 
# you can use DB Browser for SQLite.

## Alternative DB session with middleware
# If you can't use dependencies with yield 
    # for example, if you are not using Python 3.7 
    # and can't install the "backports" mentioned above for Python 3.6 
# see: [here](https://fastapi.tiangolo.com/tutorial/sql-databases/#alternative-db-session-with-middleware)
