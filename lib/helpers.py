from models import Event, Attendee, Activity
from datetime import datetime, time
import sys

# Utility functions
def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*50)
    print(f"  {title.upper()}")
    print("="*50)

def print_divider():
    """Print a divider line"""
    print("-" * 50)

def get_input(prompt, input_type=str, required=True):
    """Get validated input from user"""
    while True:
        try:
            value = input(f"{prompt}: ").strip()
            
            if not value and required:
                print("This field is required. Please enter a value.")
                continue
            elif not value and not required:
                return None
            
            if input_type == int:
                return int(value)
            elif input_type == float:
                return float(value)
            elif input_type == datetime:
                # Parse datetime in format: YYYY-MM-DD HH:MM
                return datetime.strptime(value, "%Y-%m-%d %H:%M")
            elif input_type == time:
                # Parse time in format: HH:MM
                return datetime.strptime(value, "%H:%M").time()
            else:
                return value
                
        except ValueError as e:
            if input_type == int:
                print("Please enter a valid number.")
            elif input_type == float:
                print("Please enter a valid decimal number.")
            elif input_type == datetime:
                print("Please enter date and time in format: YYYY-MM-DD HH:MM (e.g., 2024-12-25 18:00)")
            elif input_type == time:
                print("Please enter time in format: HH:MM (e.g., 14:30)")
            else:
                print(f"Invalid input: {e}")

def confirm_action(message):
    """Get user confirmation for an action"""
    while True:
        response = input(f"{message} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def wait_for_enter():
    """Wait for user to press enter"""
    input("\nPress Enter to continue...")

# Event management functions
def list_all_events():
    """Display all events in a formatted table"""
    events = Event.get_all()
    
    if not events:
        print("\n📅 No events found.")
        return []
    
    print_header("All Events")
    print(f"{'ID':<5} {'Name':<25} {'Date':<20} {'Location':<20} {'Status':<12} {'Attendees'}")
    print_divider()
    
    for event in events:
        attendee_count = event.get_attendee_count()
        date_str = event.date.strftime("%Y-%m-%d %H:%M")
        print(f"{event.id:<5} {event.name[:24]:<25} {date_str:<20} {event.location[:19]:<20} {event.status:<12} {attendee_count}")
    
    return events

def create_event():
    """Create a new event"""
    print_header("Create New Event")
    
    try:
        name = get_input("Event name")
        description = get_input("Description", required=False)
        date = get_input("Date and time", datetime)
        location = get_input("Location")
        budget = get_input("Budget (optional, default: 0)", float, required=False) or 0.0
        
        status_options = ['Planning', 'Active', 'Completed', 'Cancelled']
        print(f"\nStatus options: {', '.join(status_options)}")
        status = get_input("Status (default: Planning)", required=False) or 'Planning'
        
        if status not in status_options:
            status = 'Planning'
        
        event = Event.create(name, description, date, location, budget, status)
        print(f"\n✅ Event '{event.name}' created successfully! (ID: {event.id})")
        
    except Exception as e:
        print(f"\n❌ Error creating event: {e}")

def view_event_details():
    """View detailed information about a specific event"""
    events = list_all_events()
    if not events:
        return
    
    try:
        event_id = get_input("\nEnter event ID to view details", int)
        event = Event.find_by_id(event_id)
        
        if not event:
            print(f"\n❌ Event with ID {event_id} not found.")
            return
        
        print_header(f"Event Details - {event.name}")
        print(f"ID: {event.id}")
        print(f"Name: {event.name}")
        print(f"Description: {event.description or 'No description'}")
        print(f"Date & Time: {event.date.strftime('%Y-%m-%d %H:%M')}")
        print(f"Location: {event.location}")
        print(f"Budget: ${event.budget:.2f}")
        print(f"Status: {event.status}")
        
        # Attendee summary
        attendees = event.attendees
        confirmed = len([a for a in attendees if a.rsvp_status == 'Confirmed'])
        pending = len([a for a in attendees if a.rsvp_status == 'Pending'])
        declined = len([a for a in attendees if a.rsvp_status == 'Declined'])
        
        print(f"\n👥 Attendees: {len(attendees)} total")
        print(f"   - Confirmed: {confirmed}")
        print(f"   - Pending: {pending}")
        print(f"   - Declined: {declined}")
        
        # Activity summary
        activities = event.activities
        total_cost = event.get_total_activity_cost()
        remaining_budget = event.get_budget_remaining()
        
        print(f"\n🎯 Activities: {len(activities)} scheduled")
        print(f"   - Total cost: ${total_cost:.2f}")
        print(f"   - Budget remaining: ${remaining_budget:.2f}")
        
        if activities:
            print(f"\n📋 Activity Schedule:")
            for activity in sorted(activities, key=lambda a: a.start_time):
                end_time = activity.get_end_time()
                print(f"   • {activity.start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}: {activity.name} (${activity.cost:.2f})")
        
    except Exception as e:
        print(f"\n❌ Error viewing event details: {e}")

def delete_event():
    """Delete an event"""
    events = list_all_events()
    if not events:
        return
    
    try:
        event_id = get_input("\nEnter event ID to delete", int)
        event = Event.find_by_id(event_id)
        
        if not event:
            print(f"\n❌ Event with ID {event_id} not found.")
            return
        
        print(f"\n⚠️  You are about to delete:")
        print(f"   Event: {event.name}")
        print(f"   Date: {event.date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   This will also delete {len(event.attendees)} attendees and {len(event.activities)} activities.")
        
        if confirm_action("Are you sure you want to delete this event?"):
            event.delete()
            print(f"\n✅ Event '{event.name}' deleted successfully!")
        else:
            print("\n❌ Event deletion cancelled.")
            
    except Exception as e:
        print(f"\n❌ Error deleting event: {e}")

# Attendee management functions
def list_attendees_for_event():
    """List all attendees for a specific event"""
    events = list_all_events()
    if not events:
        return None
    
    try:
        event_id = get_input("\nEnter event ID to view attendees", int)
        event = Event.find_by_id(event_id)
        
        if not event:
            print(f"\n❌ Event with ID {event_id} not found.")
            return None
        
        attendees = event.attendees
        
        if not attendees:
            print(f"\n👥 No attendees found for event '{event.name}'.")
            return event
        
        print_header(f"Attendees for {event.name}")
        print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'RSVP':<12} {'Dietary Restrictions'}")
        print_divider()
        
        for attendee in attendees:
            restrictions = attendee.dietary_restrictions or 'None'
            print(f"{attendee.id:<5} {attendee.name[:24]:<25} {attendee.email[:29]:<30} {attendee.rsvp_status:<12} {restrictions}")
        
        return event
        
    except Exception as e:
        print(f"\n❌ Error listing attendees: {e}")
        return None

def add_attendee_to_event():
    """Add a new attendee to an event"""
    events = list_all_events()
    if not events:
        return
    
    try:
        event_id = get_input("\nEnter event ID to add attendee to", int)
        event = Event.find_by_id(event_id)
        
        if not event:
            print(f"\n❌ Event with ID {event_id} not found.")
            return
        
        print_header(f"Add Attendee to {event.name}")
        
        name = get_input("Attendee name")
        email = get_input("Email address")
        phone = get_input("Phone number (optional)", required=False)
        
        rsvp_options = ['Pending', 'Confirmed', 'Declined']
        print(f"\nRSVP options: {', '.join(rsvp_options)}")
        rsvp_status = get_input("RSVP status (default: Pending)", required=False) or 'Pending'
        
        if rsvp_status not in rsvp_options:
            rsvp_status = 'Pending'
        
        dietary = get_input("Dietary restrictions (optional)", required=False)
        
        # Check if email already exists for this event
        existing = Attendee.find_by_email(email)
        if existing and existing.event_id == event_id:
            print(f"\n❌ An attendee with email {email} already exists for this event.")
            return
        
        attendee = Attendee.create(name, email, event_id, phone, rsvp_status, dietary)
        print(f"\n✅ Attendee '{attendee.name}' added to event '{event.name}' successfully!")
        
    except Exception as e:
        print(f"\n❌ Error adding attendee: {e}")

def update_attendee_rsvp():
    """Update an attendee's RSVP status"""
    event = list_attendees_for_event()
    if not event or not event.attendees:
        return
    
    try:
        attendee_id = get_input("\nEnter attendee ID to update RSVP", int)
        attendee = Attendee.find_by_id(attendee_id)
        
        if not attendee or attendee.event_id != event.id:
            print(f"\n❌ Attendee with ID {attendee_id} not found for this event.")
            return
        
        print(f"\nCurrent RSVP status for {attendee.name}: {attendee.rsvp_status}")
        
        rsvp_options = ['Pending', 'Confirmed', 'Declined']
        print(f"RSVP options: {', '.join(rsvp_options)}")
        new_status = get_input("New RSVP status")
        
        if new_status not in rsvp_options:
            print(f"❌ Invalid RSVP status. Must be one of: {rsvp_options}")
            return
        
        attendee.update_rsvp(new_status)
        print(f"\n✅ RSVP status for {attendee.name} updated to '{new_status}'!")
        
    except Exception as e:
        print(f"\n❌ Error updating RSVP: {e}")

def delete_attendee():
    """Delete an attendee from an event"""
    event = list_attendees_for_event()
    if not event or not event.attendees:
        return
    
    try:
        attendee_id = get_input("\nEnter attendee ID to delete", int)
        attendee = Attendee.find_by_id(attendee_id)
        
        if not attendee or attendee.event_id != event.id:
            print(f"\n❌ Attendee with ID {attendee_id} not found for this event.")
            return
        
        print(f"\n⚠️  You are about to delete:")
        print(f"   Attendee: {attendee.name} ({attendee.email})")
        print(f"   From event: {event.name}")
        
        if confirm_action("Are you sure you want to delete this attendee?"):
            attendee.delete()
            print(f"\n✅ Attendee '{attendee.name}' deleted successfully!")
        else:
            print("\n❌ Attendee deletion cancelled.")
            
    except Exception as e:
        print(f"\n❌ Error deleting attendee: {e}")

# Activity management functions
def list_activities_for_event():
    """List all activities for a specific event"""
    events = list_all_events()
    if not events:
        return None
    
    try:
        event_id = get_input("\nEnter event ID to view activities", int)
        event = Event.find_by_id(event_id)
        
        if not event:
            print(f"\n❌ Event with ID {event_id} not found.")
            return None
        
        activities = event.activities
        
        if not activities:
            print(f"\n🎯 No activities found for event '{event.name}'.")
            return event
        
        print_header(f"Activities for {event.name}")
        print(f"{'ID':<5} {'Name':<25} {'Start Time':<12} {'Duration':<10} {'Cost':<10} {'Max People'}")
        print_divider()
        
        for activity in sorted(activities, key=lambda a: a.start_time):
            duration_str = f"{activity.duration}min"
            cost_str = f"${activity.cost:.2f}"
            max_p = str(activity.max_participants) if activity.max_participants else "No limit"
            print(f"{activity.id:<5} {activity.name[:24]:<25} {activity.start_time.strftime('%H:%M'):<12} {duration_str:<10} {cost_str:<10} {max_p}")
        
        return event
        
    except Exception as e:
        print(f"\n❌ Error listing activities: {e}")
        return None

def add_activity_to_event():
    """Add a new activity to an event"""
    events = list_all_events()
    if not events:
        return
    
    try:
        event_id = get_input("\nEnter event ID to add activity to", int)
        event = Event.find_by_id(event_id)
        
        if not event:
            print(f"\n❌ Event with ID {event_id} not found.")
            return
        
        print_header(f"Add Activity to {event.name}")
        
        name = get_input("Activity name")
        description = get_input("Description (optional)", required=False)
        start_time = get_input("Start time", time)
        duration = get_input("Duration in minutes", int)
        cost = get_input("Cost (optional, default: 0)", float, required=False) or 0.0
        max_participants = get_input("Maximum participants (optional)", int, required=False)
        
        # Check for time conflicts
        existing_activities = event.activities
        new_activity_temp = Activity(name=name, start_time=start_time, duration=duration, event_id=event_id)
        
        conflicts = []
        for existing in existing_activities:
            if new_activity_temp.conflicts_with(existing):
                conflicts.append(existing)
        
        if conflicts:
            print(f"\n⚠️  Time conflict detected with:")
            for conflict in conflicts:
                end_time = conflict.get_end_time()
                print(f"   • {conflict.name} ({conflict.start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')})")
            
            if not confirm_action("Do you want to add this activity anyway?"):
                print("\n❌ Activity creation cancelled.")
                return
        
        activity = Activity.create(name, start_time, duration, event_id, description, cost, max_participants)
        print(f"\n✅ Activity '{activity.name}' added to event '{event.name}' successfully!")
        
        # Check budget
        remaining_budget = event.get_budget_remaining()
        if remaining_budget < 0:
            print(f"\n⚠️  Warning: This activity puts the event over budget by ${abs(remaining_budget):.2f}!")
        
    except Exception as e:
        print(f"\n❌ Error adding activity: {e}")

def delete_activity():
    """Delete an activity from an event"""
    event = list_activities_for_event()
    if not event or not event.activities:
        return
    
    try:
        activity_id = get_input("\nEnter activity ID to delete", int)
        activity = Activity.find_by_id(activity_id)
        
        if not activity or activity.event_id != event.id:
            print(f"\n❌ Activity with ID {activity_id} not found for this event.")
            return
        
        print(f"\n⚠️  You are about to delete:")
        print(f"   Activity: {activity.name}")
        print(f"   Time: {activity.start_time.strftime('%H:%M')} ({activity.duration} minutes)")
        print(f"   Cost: ${activity.cost:.2f}")
        print(f"   From event: {event.name}")
        
        if confirm_action("Are you sure you want to delete this activity?"):
            activity.delete()
            print(f"\n✅ Activity '{activity.name}' deleted successfully!")
        else:
            print("\n❌ Activity deletion cancelled.")
            
    except Exception as e:
        print(f"\n❌ Error deleting activity: {e}")

# Dashboard and reporting functions
def show_event_dashboard():
    """Show a dashboard with event statistics"""
    events = Event.get_all()
    
    if not events:
        print("\n📊 No events to display in dashboard.")
        return
    
    print_header("Event Planning Dashboard")
    
    # Overall statistics
    total_events = len(events)
    total_attendees = sum(len(event.attendees) for event in events)
    total_activities = sum(len(event.activities) for event in events)
    total_budget = sum(event.budget for event in events)
    
    print(f"📅 Total Events: {total_events}")
    print(f"👥 Total Attendees: {total_attendees}")
    print(f"🎯 Total Activities: {total_activities}")
    print(f"💰 Total Budget: ${total_budget:.2f}")
    
    # Events by status
    status_counts = {}
    for event in events:
        status = event.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"\n📊 Events by Status:")
    for status, count in status_counts.items():
        print(f"   • {status}: {count}")
    
    # Upcoming events (next 5)
    from datetime import datetime
    now = datetime.now()
    upcoming_events = [e for e in events if e.date > now]
    upcoming_events.sort(key=lambda e: e.date)
    
    if upcoming_events:
        print(f"\n📅 Upcoming Events:")
        for event in upcoming_events[:5]:
            attendee_count = event.get_attendee_count()
            days_away = (event.date - now).days
            print(f"   • {event.name} - {event.date.strftime('%Y-%m-%d')} ({days_away} days away) - {attendee_count} confirmed")
    
    # Budget analysis
    over_budget_events = [e for e in events if e.get_budget_remaining() < 0]
    if over_budget_events:
        print(f"\n⚠️  Events Over Budget:")
        for event in over_budget_events:
            overage = abs(event.get_budget_remaining())
            print(f"   • {event.name}: Over by ${overage:.2f}")

def search_events():
    """Search for events by name"""
    search_term = get_input("Enter search term for event name")
    
    if not search_term:
        print("❌ Please enter a search term.")
        return
    
    events = Event.find_by_name(search_term)
    
    if not events:
        print(f"\n🔍 No events found matching '{search_term}'.")
        return
    
    print_header(f"Search Results for '{search_term}'")
    print(f"{'ID':<5} {'Name':<25} {'Date':<20} {'Location':<20} {'Status'}")
    print_divider()
    
    for event in events:
        date_str = event.date.strftime("%Y-%m-%d %H:%M")
        print(f"{event.id:<5} {event.name[:24]:<25} {date_str:<20} {event.location[:19]:<20} {event.status}")

def generate_event_report():
    """Generate a detailed report for a specific event"""
    events = list_all_events()
    if not events:
        return
    
    try:
        event_id = get_input("\nEnter event ID for detailed report", int)
        event = Event.find_by_id(event_id)
        
        if not event:
            print(f"\n❌ Event with ID {event_id} not found.")
            return
        
        print_header(f"Detailed Report: {event.name}")
        
        # Basic event info
        print(f"📅 Event Information:")
        print(f"   Name: {event.name}")
        print(f"   Date: {event.date.strftime('%A, %B %d, %Y at %H:%M')}")
        print(f"   Location: {event.location}")
        print(f"   Status: {event.status}")
        print(f"   Description: {event.description or 'No description provided'}")
        
        # Financial summary
        total_cost = event.get_total_activity_cost()
        remaining_budget = event.get_budget_remaining()
        
        print(f"\n💰 Financial Summary:")
        print(f"   Budget: ${event.budget:.2f}")
        print(f"   Activity Costs: ${total_cost:.2f}")
        print(f"   Remaining: ${remaining_budget:.2f}")
        
        if remaining_budget < 0:
            print(f"   ⚠️  Over Budget: ${abs(remaining_budget):.2f}")
        
        # Attendee breakdown
        attendees = event.attendees
        attendee_stats = {
            'Confirmed': [a for a in attendees if a.rsvp_status == 'Confirmed'],
            'Pending': [a for a in attendees if a.rsvp_status == 'Pending'],
            'Declined': [a for a in attendees if a.rsvp_status == 'Declined']
        }
        
        print(f"\n👥 Attendee Summary:")
        print(f"   Total Invited: {len(attendees)}")
        for status, attendee_list in attendee_stats.items():
            print(f"   {status}: {len(attendee_list)}")
        
        # Dietary restrictions summary
        dietary_restrictions = [a.dietary_restrictions for a in attendees if a.dietary_restrictions and a.rsvp_status == 'Confirmed']
        if dietary_restrictions:
            print(f"\n🍽️  Dietary Restrictions (Confirmed attendees):")
            dietary_counts = {}
            for restriction in dietary_restrictions:
                dietary_counts[restriction] = dietary_counts.get(restriction, 0) + 1
            for restriction, count in dietary_counts.items():
                print(f"   • {restriction}: {count} attendee(s)")
        
        # Activity schedule
        activities = sorted(event.activities, key=lambda a: a.start_time)
        if activities:
            print(f"\n🎯 Activity Schedule:")
            for activity in activities:
                end_time = activity.get_end_time()
                max_p = f" (max {activity.max_participants})" if activity.max_participants else ""
                print(f"   • {activity.start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}: {activity.name}{max_p}")
                if activity.description:
                    print(f"     {activity.description}")
                if activity.cost > 0:
                    print(f"     Cost: ${activity.cost:.2f}")
        
        # Time conflicts
        conflicts = []
        for i, activity1 in enumerate(activities):
            for activity2 in activities[i+1:]:
                if activity1.conflicts_with(activity2):
                    conflicts.append((activity1, activity2))
        
        if conflicts:
            print(f"\n⚠️  Time Conflicts Detected:")
            for act1, act2 in conflicts:
                print(f"   • {act1.name} conflicts with {act2.name}")
        
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")

# Application control functions
def exit_program():
    """Exit the application"""
    print("\n👋 Thank you for using Event Planner!")
    print("Goodbye!")
    sys.exit(0)