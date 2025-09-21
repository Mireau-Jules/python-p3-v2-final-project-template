# Event Planner CLI

A comprehensive command-line interface application for managing events, attendees, and activities. Built with Python, SQLAlchemy ORM, and designed with user experience in mind.

## 🎯 Overview

Event Planner CLI is a professional-grade event management system that allows event planners to efficiently organize events, manage attendee lists, schedule activities, and track budgets. The application features an intuitive menu-driven interface that hides technical complexity while providing powerful functionality.

## ✨ Features

### 📅 Event Management
- Create, view, update, and delete events
- Track event details: name, description, date, location, budget, status
- View comprehensive event summaries with attendee and activity counts
- Search events by name
- Budget tracking and over-budget warnings

### 👥 Attendee Management
- Add attendees to specific events with context-aware navigation
- Manage RSVP status (Pending, Confirmed, Declined)
- Track contact information and dietary restrictions
- Email validation and duplicate prevention
- View attendee lists organized by event

### 🎯 Activity Management
- Schedule activities with start times and duration
- Cost tracking for budget management
- Maximum participant limits
- Automatic time conflict detection
- Activity scheduling within event context

### 📊 Dashboard & Reporting
- Real-time dashboard with event statistics
- Upcoming events overview
- Budget analysis and over-budget alerts
- Detailed event reports with financial summaries
- Attendee breakdown by RSVP status
- Dietary restrictions summary for catering

## 🏗️ Project Structure

```
event-planner-cli/
├── Pipfile                 # Python dependencies
├── Pipfile.lock           # Locked dependencies
├── README.md              # Project documentation
└── lib/
    ├── models/
    │   ├── __init__.py    # Database configuration
    │   ├── event.py       # Event model with ORM methods
    │   ├── attendee.py    # Attendee model with validation
    │   └── activity.py    # Activity model with conflict detection
    ├── cli.py             # Main CLI interface
    ├── helpers.py         # Helper functions and business logic
    └── debug.py           # Debug utilities and sample data
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Pipenv (for dependency management)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd event-planner-cli
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Activate virtual environment**
   ```bash
   pipenv shell
   ```

4. **Run the application**
   ```bash
   python lib/cli.py
   ```

### Optional: Create Sample Data

To populate the database with sample events, attendees, and activities for testing:

```bash
python lib/debug.py
# Select option 1 to initialize database
# Select option 3 to create sample data
```

## 💻 Usage

### Starting the Application

Run the main CLI application:
```bash
python lib/cli.py
```

You'll be greeted with the main menu offering six primary functions:

1. **📅 Manage Events** - Create, view, and delete events
2. **👥 Manage Attendees** - Add and manage event attendees
3. **🎯 Manage Activities** - Schedule and organize event activities
4. **📊 Event Dashboard** - View statistics and upcoming events
5. **🔍 Search Events** - Find events by name
6. **📋 Generate Event Report** - Create detailed event reports

### User Experience Highlights

**Context-Aware Navigation**: When viewing a specific event, you can add attendees or activities directly to that event without re-selecting it.

**Input Validation**: The system validates all input including:
- Email format validation
- Date and time format checking
- Budget and cost validation (no negative values)
- RSVP status validation

**Smart Features**:
- Automatic time conflict detection for activities
- Budget tracking with over-budget warnings
- Attendee count tracking by RSVP status
- Dietary restrictions compilation for catering

### Sample Workflow

1. **Create an Event**
   - Navigate to "Manage Events" → "Create New Event"
   - Enter event details (name, date, location, budget)
   - System creates event and returns to menu

2. **Add Attendees**
   - Navigate to "Manage Attendees" → "Add New Attendee"
   - Select the event from the list
   - Enter attendee information with automatic email validation
   - Set initial RSVP status

3. **Schedule Activities**
   - Navigate to "Manage Activities" → "Add New Activity"
   - Select the target event
   - Schedule activity with automatic conflict detection
   - System warns if activity exceeds remaining budget

4. **Monitor Progress**
   - Use "Event Dashboard" for overall statistics
   - Generate detailed reports for specific events
   - Track confirmed attendees and budget utilization

## 🏛️ Database Schema

### Tables and Relationships

**Events** (Primary Entity)
- `id` (Primary Key)
- `name`, `description`, `date`, `location`
- `budget`, `status`

**Attendees** (One-to-Many with Events)
- `id` (Primary Key)
- `name`, `email`, `phone`
- `rsvp_status`, `dietary_restrictions`
- `event_id` (Foreign Key → Events)

**Activities** (One-to-Many with Events)
- `id` (Primary Key)
- `name`, `description`, `start_time`, `duration`
- `cost`, `max_participants`
- `event_id` (Foreign Key → Events)

### Data Relationships
- Each Event can have multiple Attendees and Activities
- Each Attendee belongs to exactly one Event
- Each Activity belongs to exactly one Event
- Cascade deletion: Deleting an Event removes all associated Attendees and Activities

## 🔧 Technical Implementation

### Models (`lib/models/`)

**`event.py`** - Event Model
- Implements full CRUD operations (Create, Read, Update, Delete)
- Property validation for name, location, and budget
- Business logic methods: `get_attendee_count()`, `get_total_activity_cost()`, `get_budget_remaining()`
- Search functionality by name and ID

**`attendee.py`** - Attendee Model  
- Email format validation using regex
- RSVP status validation (Pending, Confirmed, Declined)
- Relationship management with Events
- Search capabilities by name, email, and event association

**`activity.py`** - Activity Model
- Time and duration validation
- Cost and participant limit management
- Time conflict detection between activities
- Integration with Event budget tracking

### CLI Interface (`lib/cli.py`)

The CLI follows a hierarchical menu structure:
- **Main Menu**: Primary navigation hub
- **Management Submenus**: Focused workflows for Events, Attendees, and Activities
- **Context Preservation**: Users stay within relevant contexts (e.g., when managing attendees for a specific event)

Key design principles:
- **User-Centric**: Hides database IDs and technical details from users
- **Error Handling**: Graceful handling of invalid input with helpful error messages
- **Confirmation Prompts**: Prevents accidental deletions with confirmation dialogs

### Helper Functions (`lib/helpers.py`)

**Utility Functions**:
- `clear_screen()`: Cross-platform screen clearing
- `print_header()`: Consistent formatting for section headers
- `get_input()`: Validated input collection with type conversion
- `confirm_action()`: User confirmation for destructive operations

**Business Logic Functions**:
- Event management: Create, view, delete events with full validation
- Attendee management: Context-aware attendee handling
- Activity management: Scheduling with conflict detection
- Dashboard and reporting: Statistical analysis and report generation

### Debug Utilities (`lib/debug.py`)

Development and testing support:
- Database initialization and cleanup
- Sample data generation for testing
- ORM method testing
- Database statistics and health checks

## 🎨 User Experience Design

### Design Philosophy
- **Hide Complexity**: Users never see database IDs, raw objects, or technical errors
- **Contextual Actions**: When browsing desserts, you can add a dessert recipe without re-selecting the category
- **Informative Feedback**: Clear success/error messages with actionable guidance
- **Professional Formatting**: Clean tables and headers for easy reading

### Data Structures Used
- **Lists**: Event collections, attendee lists, activity schedules
- **Dictionaries**: RSVP status counts, dietary restriction summaries, validation mappings
- **Tuples**: Time conflict pairs, coordinate data for reports

### Input Validation Strategy
- **Progressive Validation**: Check format, then business rules, then constraints
- **Helpful Error Messages**: Specific guidance rather than generic "Invalid input"
- **Graceful Degradation**: Allow partial completion and provide defaults where appropriate

## 🧪 Testing

### Manual Testing Approach
The application is designed for comprehensive manual testing through the CLI interface:

1. **Data Validation Testing**
   - Enter invalid emails, negative budgets, malformed dates
   - Verify appropriate error messages and recovery

2. **Business Logic Testing**
   - Create time conflicts between activities
   - Exceed event budgets with activities
   - Test cascade deletions

3. **User Experience Testing**
   - Navigate through complete workflows
   - Test context preservation and menu navigation
   - Verify report accuracy and formatting

### Using Debug Mode
```bash
python lib/debug.py
```
Use debug mode to:
- Create comprehensive test data
- Verify ORM relationships
- Test edge cases and error conditions

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes following the established patterns
4. Test thoroughly using the CLI and debug utilities
5. Submit a pull request

### Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Include docstrings for all functions and classes
- Maintain separation of concerns between models, CLI, and helpers

### Adding New Features
When adding new functionality:
1. Update the appropriate model with new ORM methods
2. Add helper functions for business logic
3. Integrate into the CLI menu system
4. Update this README with new feature documentation
5. Add relevant test cases to debug utilities

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Built as part of the Flatiron School Phase 3 curriculum, demonstrating:
- Python fundamentals and object-oriented programming
- SQLAlchemy ORM with complex relationships
- CLI design and user experience principles
- Database design and management
- Professional code organization and documentation

---

*Event Planner CLI - Making event management simple and efficient.*