from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, SESSION

class Attendee(Base):
    __tablename__ = 'attendees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    rsvp_status = Column(String, default='Pending')
    dietary_restrictions = Column(String)
    event_id = Column(Integer, ForeignKey('events.id'))
    
    # Relationships
    event = relationship('Event', back_populates='attendees')
    
    def __repr__(self):
        return f"<Attendee(id={self.id}, name='{self.name}', email='{self.email}', status='{self.rsvp_status}')>"
    
    def __init__(self, **kwargs):
        # Validate email and name before setting
        if 'email' in kwargs and not self._is_valid_email(kwargs['email']):
            raise ValueError("Invalid email format")
        if 'name' in kwargs and (not isinstance(kwargs['name'], str) or len(kwargs['name'].strip()) == 0):
            raise ValueError("Attendee name must be a non-empty string")
        if 'rsvp_status' in kwargs:
            valid_statuses = ['Pending', 'Confirmed', 'Declined']
            if kwargs['rsvp_status'] not in valid_statuses:
                raise ValueError(f"RSVP status must be one of: {valid_statuses}")
        
        # Set attributes
        for key, value in kwargs.items():
            if key == 'email':
                value = value.strip().lower()
            elif key == 'name':
                value = value.strip()
            setattr(self, key, value)
    
    def _is_valid_email(self, email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # ORM Methods
    @classmethod
    def create(cls, name, email, event_id, phone=None, rsvp_status='Pending', dietary_restrictions=None):
        """Create a new attendee"""
        session = SESSION()
        try:
            attendee = cls(
                name=name,
                email=email,
                event_id=event_id,
                phone=phone,
                rsvp_status=rsvp_status,
                dietary_restrictions=dietary_restrictions
            )
            session.add(attendee)
            session.commit()
            return attendee
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self):
        """Delete this attendee"""
        session = SESSION()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all attendees"""
        session = SESSION()
        attendees = session.query(cls).all()
        session.close()
        return attendees
    
    @classmethod
    def find_by_id(cls, attendee_id):
        """Find attendee by ID"""
        session = SESSION()
        attendee = session.query(cls).filter(cls.id == attendee_id).first()
        session.close()
        return attendee
    
    @classmethod
    def find_by_event(cls, event_id):
        """Find all attendees for an event"""
        session = SESSION()
        attendees = session.query(cls).filter(cls.event_id == event_id).all()
        session.close()
        return attendees
    
    @classmethod
    def find_by_name(cls, name):
        """Find attendees by name (partial match)"""
        session = SESSION()
        attendees = session.query(cls).filter(cls.name.ilike(f'%{name}%')).all()
        session.close()
        return attendees
    
    @classmethod
    def find_by_email(cls, email):
        """Find attendee by email"""
        session = SESSION()
        attendee = session.query(cls).filter(cls.email == email.lower()).first()
        session.close()
        return attendee
    
    def update_rsvp(self, status):
        """Update RSVP status"""
        valid_statuses = ['Pending', 'Confirmed', 'Declined']
        if status not in valid_statuses:
            raise ValueError(f"RSVP status must be one of: {valid_statuses}")
            
        session = SESSION()
        try:
            self.rsvp_status = status
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
        return re.match(pattern, email) is not None
    
    # ORM Methods
    @classmethod
    def create(cls, name, email, event_id, phone=None, rsvp_status='Pending', dietary_restrictions=None):
        """Create a new attendee"""
        session = SESSION()
        try:
            attendee = cls(
                name=name,
                email=email,
                event_id=event_id,
                phone=phone,
                rsvp_status=rsvp_status,
                dietary_restrictions=dietary_restrictions
            )
            session.add(attendee)
            session.commit()
            return attendee
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self):
        """Delete this attendee"""
        session = SESSION()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all attendees"""
        session = SESSION()
        attendees = session.query(cls).all()
        session.close()
        return attendees
    
    @classmethod
    def find_by_id(cls, attendee_id):
        """Find attendee by ID"""
        session = SESSION()
        attendee = session.query(cls).filter(cls.id == attendee_id).first()
        session.close()
        return attendee
    
    @classmethod
    def find_by_event(cls, event_id):
        """Find all attendees for an event"""
        session = SESSION()
        attendees = session.query(cls).filter(cls.event_id == event_id).all()
        session.close()
        return attendees
    
    @classmethod
    def find_by_name(cls, name):
        """Find attendees by name (partial match)"""
        session = SESSION()
        attendees = session.query(cls).filter(cls.name.ilike(f'%{name}%')).all()
        session.close()
        return attendees
    
    @classmethod
    def find_by_email(cls, email):
        """Find attendee by email"""
        session = SESSION()
        attendee = session.query(cls).filter(cls.email == email.lower()).first()
        session.close()
        return attendee
    
    def update_rsvp(self, status):
        """Update RSVP status"""
        session = SESSION()
        try:
            self.rsvp_status = status
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()