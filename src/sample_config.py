# DB URI
# example DB URI:
# mysql+oursql://scott:tiger@localhost/mydatabase
# postgresql+psycopg2://scott:tiger@localhost/mydatabase
SQLALCHEMY_DATABASE_URI =\
    'dialect+driver://username:password@host:port/database'

# Debug from SQLAlchemy
# Turn this to False on production
SQLALCHEMY_ECHO = False

# List of allowed origins for CORS
ALLOWED_ORIGINS = ['*.virtual-labs.ac.in']

# Configure your log paths
LOG_FILE = 'logs/dataservice.log'

# Log level for the application
LOG_LEVEL = 'ERROR'
