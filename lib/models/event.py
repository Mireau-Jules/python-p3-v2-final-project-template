from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from . import Base, SESSION
from datetime import datetime

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    budget = Column(Float, default=0.0)
    status = Column(String, default='Planning')
    
    # Relationships
    attendees = relationship('Attendee', back_populates='event', cascade='all, delete-orphan')
    activities = relationship('Activity', back_populates='event', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', date='{self.date}', location='{self.location}')>"
    
    def __init__(self, **kwargs):
        # Set defaults and validate
        for key, value in kwargs.items():
            if key == 'name' and (not isinstance(value, str) or len(value.strip()) == 0):
                raise ValueError("Event name must be a non-empty string")
            elif key == 'location' and (not isinstance(value, str) or len(value.strip()) == 0):
                raise ValueError("Event location must be a non-empty string")
            elif key == 'budget' and value < 0:
                raise ValueError("Budget cannot be negative")
            setattr(self, key, value)
    
    # ORM Methods
    @classmethod
    def create(cls, name, description, date, location, budget=0.0, status='Planning'):
        """Create a new event"""
        session = SESSION()
        try:
            event = cls(
                name=name,
                description=description,
                date=date,
                location=location,
                budget=budget,
                status=status
            )
            session.add(event)
            session.commit()
            session.refresh(event)  # Refresh to get the ID
            return event
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self):
        """Delete this event"""
        session = SESSION()
        try:
            # Reattach to session
            event_to_delete = session.merge(self)
            session.delete(event_to_delete)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all events"""
        session = SESSION()
        try:
            events = session.query(cls).all()
            # Make sure we can access relationships after session closes
            for event in events:
                _ = len(event.attendees)  # Force load attendees
                _ = len(event.activities)  # Force load activities
            return events
        finally:
            session.close()
    
    @classmethod
    def find_by_id(cls, event_id):
        """Find event by ID"""
        session = SESSION()
        try:
            event = session.query(cls).filter(cls.id == event_id).first()
            if event:
                # Force load relationships
                _ = len(event.attendees)
                _ = len(event.activities)
            return event
        finally:
            session.close()
    
    @classmethod
    def find_by_name(cls, name):
        """Find events by name (partial match)"""
        session = SESSION()
        try:
            events = session.query(cls).filter(cls.name.ilike(f'%{name}%')).all()
            # Force load relationships
            for event in events:
                _ = len(event.attendees)
                _ = len(event.activities)
            return events
        finally:
            session.close()
    
    def get_attendee_count(self):
        """Get count of confirmed attendees"""
        try:
            return len([a for a in self.attendees if a.rsvp_status == 'Confirmed'])
        except:
            # If attendees not loaded, query separately
            from .attendee import Attendee
            session = SESSION()
            try:
                count = session.query(Attendee).filter(
                    Attendee.event_id == self.id,
                    Attendee.rsvp_status == 'Confirmed'
                ).count()
                return count
            finally:
                session.close()
    
    def get_total_activity_cost(self):
        """Calculate total cost of all activities"""
        try:
            return sum(activity.cost for activity in self.activities)
        except:
            # If activities not loaded, query separately
            from .activity import Activity
            session = SESSION()
            try:
                from sqlalchemy import func
                total = session.query(func.sum(Activity.cost)).filter(
                    Activity.event_id == self.id
                ).scalar()
                return total or 0.0
            finally:
                session.close()
    
    def get_budget_remaining(self):
        """Calculate remaining budget after activities"""
        return self.budget - self.get_total_activity_cost()