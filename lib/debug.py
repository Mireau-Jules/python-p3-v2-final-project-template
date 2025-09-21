#!/usr/bin/env python3

"""
Debug helper script for Event Planner CLI
Use this script to test ORM methods and populate sample data
"""

from models import Base, ENGINE, SESSION, Event, Attendee, Activity
from datetime import datetime, time

def init_db():
    """Initialize the database with tables"""
    Base.metadata.create_all(ENGINE)
    print("✅ Database tables created successfully!")

def clear_db():
    """Clear all data from the database"""
    session = SESSION()
    try:
        session.query(Activity).delete()
        session.query(Attendee).delete()
        session.query(Event).delete()
        session.commit()
        print("✅ All data cleared from database!")
    except Exception as e:
        session.rollback()
        print(f"❌ Error clearing database: {e}")
    finally:
        session.close()

def create_sample_data():
    """Create sample data for testing"""
    try:
        # Create sample events
        event1 = Event.create(
            name="Tech Conference 2024",
            description="Annual technology conference with keynote speakers and workshops",
            date=datetime(2024, 6, 15, 9, 0),
            location="Convention Center Downtown",
            budget=5000.00,
            status="Planning"
        )
        
        event2 = Event.create(
            name="Summer Wedding Reception",
            description="Beautiful outdoor wedding celebration",
            date=datetime(2024, 7, 20, 17, 30),
            location="Sunset Gardens",
            budget=8000.00,
            status="Active"
        )
        
        event3 = Event.create(
            name="Company Holiday Party",
            description="Annual holiday celebration for all employees",
            date=datetime(2024, 12, 15, 18, 0),
            location="Grand Ballroom Hotel",
            budget=3000.00,
            status="Planning"
        )
        
        # Create sample attendees for event1
        attendee1 = Attendee.create(
            name="John Smith",
            email="john.smith@email.com",
            event_id=event1.id,
            phone="555-0101",
            rsvp_status="Confirmed",
            dietary_restrictions="Vegetarian"
        )
        
        attendee2 = Attendee.create(
            name="Sarah Johnson",
            email="sarah.johnson@email.com",
            event_id=event1.id,
            phone="555-0102",
            rsvp_status="Confirmed"
        )
        
        attendee3 = Attendee.create(
            name="Mike Davis",
            email="mike.davis@email.com",
            event_id=event1.id,
            rsvp_status="Pending",
            dietary_restrictions="Gluten-free"
        )
        
        # Create sample attendees for event2
        attendee4 = Attendee.create(
            name="Emily Wilson",
            email="emily.wilson@email.com",
            event_id=event2.id,
            phone="555-0201",
            rsvp_status="Confirmed"
        )
        
        attendee5 = Attendee.create(
            name="Robert Brown",
            email="robert.brown@email.com",
            event_id=event2.id,
            rsvp_status="Declined"
        )
        
        # Create sample activities for event1
        activity1 = Activity.create(
            name="Opening Keynote",
            description="Welcome address and industry overview",
            start_time=time(9, 0),
            duration=60,
            event_id=event1.id,
            cost=500.00
        )
        
        activity2 = Activity.create(
            name="Workshop: AI in Business",
            description="Hands-on workshop about AI applications",
            start_time=time(10, 30),
            duration=90,
            event_id=event1.id,
            cost=200.00,
            max_participants=30
        )
        
        activity3 = Activity.create(
            name="Networking Lunch",
            description="Catered lunch with networking opportunities",
            start_time=time(12, 0),
            duration=60,
            event_id=event1.id,
            cost=800.00
        )
        
        # Create sample activities for event2
        activity4 = Activity.create(
            name="Cocktail Hour",
            description="Pre-dinner drinks and appetizers",
            start_time=time(17, 30),
            duration=60,
            event_id=event2.id,
            cost=1200.00
        )
        
        activity5 = Activity.create(
            name="Wedding Dinner",
            description="Three-course dinner with wine pairing",
            start_time=time(18, 30),
            duration=90,
            event_id=event2.id,
            cost=2500.00
        )
        
        activity6 = Activity.create(
            name="Dancing & Entertainment",
            description="Live band and DJ for dancing",
            start_time=time(20, 0),
            duration=180,
            event_id=event2.id,
            cost=1500.00
        )
        
        print("✅ Sample data created successfully!")
        print(f"   - {len(Event.get_all())} events created")
        print(f"   - {len(Attendee.get_all())} attendees created")
        print(f"   - {len(Activity.get_all())} activities created")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

def test_orm_methods():
    """Test all ORM methods"""
    print("🧪 Testing ORM Methods")
    print("=" * 40)
    
    # Test Event methods
    print("\n📅 Testing Event methods:")
    events = Event.get_all()
    print(f"   - Total events: {len(events)}")
    
    if events:
        first_event = events[0]
        print(f"   - First event: {first_event.name}")
        print(f"   - Attendee count: {first_event.get_attendee_count()}")
        print(f"   - Activity cost: ${first_event.get_total_activity_cost():.2f}")
        print(f"   - Budget remaining: ${first_event.get_budget_remaining():.2f}")
    
    # Test search methods
    print("\n🔍 Testing search methods:")
    tech_events = Event.find_by_name("Tech")
    print(f"   - Events with 'Tech' in name: {len(tech_events)}")
    
    conf_attendees = Attendee.find_by_name("John")
    print(f"   - Attendees with 'John' in name: {len(conf_attendees)}")
    
    # Test relationships
    print("\n🔗 Testing relationships:")
    if events:
        event = events[0]
        print(f"   - Event '{event.name}' has {len(event.attendees)} attendees")
        print(f"   - Event '{event.name}' has {len(event.activities)} activities")
        
        if event.attendees:
            attendee = event.attendees[0]
            print(f"   - Attendee '{attendee.name}' belongs to event '{attendee.event.name}'")
        
        if event.activities:
            activity = event.activities[0]
            print(f"   - Activity '{activity.name}' belongs to event '{activity.event.name}'")

def show_database_stats():
    """Show current database statistics"""
    events = Event.get_all()
    attendees = Attendee.get_all()
    activities = Activity.get_all()
    
    print("📊 Database Statistics")
    print("=" * 30)
    print(f"Events: {len(events)}")
    print(f"Attendees: {len(attendees)}")
    print(f"Activities: {len(activities)}")
    
    if events:
        total_budget = sum(e.budget for e in events)
        total_cost = sum(e.get_total_activity_cost() for e in events)
        print(f"Total Budget: ${total_budget:.2f}")
        print(f"Total Activity Costs: ${total_cost:.2f}")

def main():
    """Main debug menu"""
    while True:
        print("\n" + "="*50)
        print("🔧 EVENT PLANNER DEBUG MENU")
        print("="*50)
        print("1. Initialize Database")
        print("2. Clear All Data")
        print("3. Create Sample Data")
        print("4. Test ORM Methods")
        print("5. Show Database Stats")
        print("0. Exit")
        
        try:
            choice = int(input("\nSelect option: ").strip())
            
            if choice == 0:
                print("👋 Goodbye!")
                break
            elif choice == 1:
                init_db()
            elif choice == 2:
                if input("⚠️  Are you sure? (yes/no): ").lower() == 'yes':
                    clear_db()
                else:
                    print("❌ Operation cancelled.")
            elif choice == 3:
                create_sample_data()
            elif choice == 4:
                test_orm_methods()
            elif choice == 5:
                show_database_stats()
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()