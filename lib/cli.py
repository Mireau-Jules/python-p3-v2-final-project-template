#!/usr/bin/env python3

from helpers import (
    # Utility functions
    clear_screen, print_header, wait_for_enter, get_input,
    # Event functions
    list_all_events, create_event, view_event_details, delete_event,
    # Attendee functions  
    list_attendees_for_event, add_attendee_to_event, update_attendee_rsvp, delete_attendee,
    # Activity functions
    list_activities_for_event, add_activity_to_event, delete_activity,
    # Dashboard and reporting
    show_event_dashboard, search_events, generate_event_report,
    # System functions
    exit_program
)

def main():
    """Main application loop"""
    # Initialize database
    from models import Base, ENGINE
    Base.metadata.create_all(ENGINE)
    
    clear_screen()
    print("🎉 Welcome to Event Planner CLI!")
    print("Your complete solution for managing events, attendees, and activities.")
    
    while True:
        try:
            main_menu()
            choice = get_input("\nSelect an option", int)
            
            if choice == 0:
                exit_program()
            elif choice == 1:
                event_management_menu()
            elif choice == 2:
                attendee_management_menu()
            elif choice == 3:
                activity_management_menu()
            elif choice == 4:
                show_event_dashboard()
                wait_for_enter()
            elif choice == 5:
                search_events()
                wait_for_enter()
            elif choice == 6:
                generate_event_report()
                wait_for_enter()
            else:
                print("❌ Invalid choice. Please select a number from the menu.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            wait_for_enter()

def main_menu():
    """Display the main menu"""
    clear_screen()
    print_header("Event Planner - Main Menu")
    print("1. 📅 Manage Events")
    print("2. 👥 Manage Attendees")
    print("3. 🎯 Manage Activities")
    print("4. 📊 Event Dashboard")
    print("5. 🔍 Search Events")
    print("6. 📋 Generate Event Report")
    print("0. 🚪 Exit")

def event_management_menu():
    """Event management submenu"""
    while True:
        try:
            clear_screen()
            print_header("Event Management")
            print("1. 📅 View All Events")
            print("2. ➕ Create New Event")
            print("3. 👁️  View Event Details")
            print("4. 🗑️  Delete Event")
            print("0. ⬅️  Back to Main Menu")
            
            choice = get_input("\nSelect an option", int)
            
            if choice == 0:
                break
            elif choice == 1:
                list_all_events()
                wait_for_enter()
            elif choice == 2:
                create_event()
                wait_for_enter()
            elif choice == 3:
                view_event_details()
                wait_for_enter()
            elif choice == 4:
                delete_event()
                wait_for_enter()
            else:
                print("❌ Invalid choice. Please select a number from the menu.")
                wait_for_enter()
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            wait_for_enter()

def attendee_management_menu():
    """Attendee management submenu"""
    while True:
        try:
            clear_screen()
            print_header("Attendee Management")
            print("1. 👥 View Attendees by Event")
            print("2. ➕ Add New Attendee")
            print("3. 📝 Update RSVP Status")
            print("4. 🗑️  Remove Attendee")
            print("0. ⬅️  Back to Main Menu")
            
            choice = get_input("\nSelect an option", int)
            
            if choice == 0:
                break
            elif choice == 1:
                list_attendees_for_event()
                wait_for_enter()
            elif choice == 2:
                add_attendee_to_event()
                wait_for_enter()
            elif choice == 3:
                update_attendee_rsvp()
                wait_for_enter()
            elif choice == 4:
                delete_attendee()
                wait_for_enter()
            else:
                print("❌ Invalid choice. Please select a number from the menu.")
                wait_for_enter()
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            wait_for_enter()

def activity_management_menu():
    """Activity management submenu"""
    while True:
        try:
            clear_screen()
            print_header("Activity Management")
            print("1. 🎯 View Activities by Event")
            print("2. ➕ Add New Activity")
            print("3. 🗑️  Delete Activity")
            print("0. ⬅️  Back to Main Menu")
            
            choice = get_input("\nSelect an option", int)
            
            if choice == 0:
                break
            elif choice == 1:
                list_activities_for_event()
                wait_for_enter()
            elif choice == 2:
                add_activity_to_event()
                wait_for_enter()
            elif choice == 3:
                delete_activity()
                wait_for_enter()
            else:
                print("❌ Invalid choice. Please select a number from the menu.")
                wait_for_enter()
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            wait_for_enter()

if __name__ == "__main__":
    main()