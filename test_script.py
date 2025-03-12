from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Role, Audition, Base

# Set up the database
engine = create_engine("sqlite:///moringa_theater.db")
Base.metadata.create_all(engine)  # Ensure tables exist
Session = sessionmaker(bind=engine)
session = Session()

# Clear previous test data
session.query(Audition).delete()
session.query(Role).delete()
session.commit()

# Create a role
hamlet = Role(character_name="Hamlet")
session.add(hamlet)
session.commit()

# Add auditions
audition1 = Audition(actor="John Doe", location="New York", phone=1234567890, role=hamlet)
audition2 = Audition(actor="Jane Smith", location="Los Angeles", phone=9876543210, role=hamlet)
session.add_all([audition1, audition2])
session.commit()

# Callback an audition (hire)
audition1.call_back()
session.commit()

# Test queries
print("Actors:", hamlet.actors())  # ["John Doe", "Jane Smith"]
print("Lead Actor:", hamlet.lead().actor if isinstance(hamlet.lead(), Audition) else hamlet.lead())  # "John Doe"
print("Understudy:", hamlet.understudy().actor if isinstance(hamlet.understudy(), Audition) else hamlet.understudy())  # "no actor has been hired for understudy for this role"

# Close the session
session.close()
