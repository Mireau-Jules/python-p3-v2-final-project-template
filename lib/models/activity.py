from sqlalchemy import Column, Integer, String, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from . import Base, SESSION
from datetime import time

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    cost = Column(Float, default=0.0)
    max_participants = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.id'))
    
    # Relationships
    event = relationship('Event', back_populates='activities')
    
    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}', time='{self.start_time}', duration={self.duration}min)>"
    
    def __init__(self, **kwargs):
        # Validate inputs before setting
        if 'name' in kwargs and (not isinstance(kwargs['name'], str) or len(kwargs['name'].strip()) == 0):
            raise ValueError("Activity name must be a non-empty string")
        if 'duration' in kwargs and (not isinstance(kwargs['duration'], int) or kwargs['duration'] <= 0):
            raise ValueError("Duration must be a positive integer (minutes)")
        if 'cost' in kwargs and kwargs['cost'] < 0:
            raise ValueError("Cost cannot be negative")
        if 'max_participants' in kwargs and kwargs['max_participants'] is not None:
            if not isinstance(kwargs['max_participants'], int) or kwargs['max_participants'] <= 0:
                raise ValueError("Max participants must be a positive integer or None")
        
        # Set attributes
        for key, value in kwargs.items():
            if key == 'name':
                value = value.strip()
            elif key == 'cost':
                value = float(value)
            setattr(self, key, value)
    
    # ORM Methods
    @classmethod
    def create(cls, name, start_time, duration, event_id, description=None, cost=0.0, max_participants=None):
        """Create a new activity"""
        session = SESSION()
        try:
            activity = cls(
                name=name,
                description=description,
                start_time=start_time,
                duration=duration,
                cost=cost,
                max_participants=max_participants,
                event_id=event_id
            )
            session.add(activity)
            session.commit()
            return activity
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self):
        """Delete this activity"""
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
        """Get all activities"""
        session = SESSION()
        activities = session.query(cls).all()
        session.close()
        return activities
    
    @classmethod
    def find_by_id(cls, activity_id):
        """Find activity by ID"""
        session = SESSION()
        activity = session.query(cls).filter(cls.id == activity_id).first()
        session.close()
        return activity
    
    @classmethod
    def find_by_event(cls, event_id):
        """Find all activities for an event"""
        session = SESSION()
        activities = session.query(cls).filter(cls.event_id == event_id).all()
        session.close()
        return activities
    
    @classmethod
    def find_by_name(cls, name):
        """Find activities by name (partial match)"""
        session = SESSION()
        activities = session.query(cls).filter(cls.name.ilike(f'%{name}%')).all()
        session.close()
        return activities
    
    def get_end_time(self):
        """Calculate end time based on start time and duration"""
        from datetime import datetime, timedelta
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = start_datetime + timedelta(minutes=self.duration)
        return end_datetime.time()
    
    def conflicts_with(self, other_activity):
        """Check if this activity conflicts with another activity"""
        if not isinstance(other_activity, Activity):
            return False
        
        # Convert times to minutes for easier comparison
        self_start = self.start_time.hour * 60 + self.start_time.minute
        self_end = self_start + self.duration
        
        other_start = other_activity.start_time.hour * 60 + other_activity.start_time.minute
        other_end = other_start + other_activity.duration
        
        # Check for overlap
        return not (self_end <= other_start or other_end <= self_start)