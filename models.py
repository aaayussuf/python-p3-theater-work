from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)

    auditions = relationship("Audition", back_populates="role", cascade="all, delete-orphan")

    def actors(self):
        """Returns a list of actor names for this role."""
        return [audition.actor for audition in self.auditions]

    def locations(self):
        """Returns a list of locations from auditions associated with this role."""
        return [audition.location for audition in self.auditions]

    def lead(self):
        """Returns the first hired audition or a message if none found."""
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else "no actor has been hired for this role"

    def understudy(self):
        """Returns the second hired audition or a message if none found."""
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "no actor has been hired for understudy for this role"

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        """Sets the hired attribute to True."""
        self.hired = True

