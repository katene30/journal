# Journal Entry Tracker

## Overview

Journal Entry Tracker is a Django-powered web application designed to help users monitor and manage their mental health. The platform allows users to record daily journal entries, tracking various metrics such as mood, depression, anxiety, stress levels, sleep quality, physical activity, and more. By maintaining these records, users can visualize trends over time and gain insights into their mental well-being.

## Key Features

- **User Authentication**: Secure user registration and login functionality.
- **Daily Journal Entries**: Record detailed daily entries with metrics including mood, depression, anxiety, stress, sleep, energy levels, physical activity, and more.
- **Data Visualization**: Graphs and charts to visualize trends in mental health metrics over time.
- **Reminders**: Set up daily reminders to encourage consistent journaling.
- **Export Data**: Export journal entries to CSV for further analysis.
- **Responsive Design**: User-friendly interface that works on both desktop and mobile devices.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 3.2+
- Virtual environment (recommended)

### Installation

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/yourusername/journal-entry-tracker.git
    cd journal-entry-tracker
    ```

2. **Update Env File**:

    ```sh
    cp example.env .env
    ```

3. **Set Up Virtual Environment**:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

4. **Install Dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

5. **Apply Migrations**:

    ```sh
    python manage.py migrate
    ```

6. **Create a Superuser** (for accessing the admin panel):

    ```sh
    python manage.py createsuperuser
    ```

7. **Run the Development Server**:

    ```sh
    python manage.py runserver
    ```

8. **Access the Application**:

    Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

- **Create an Account**: Sign up for a new account to start using the journal.
- **Add Journal Entries**: Log your daily metrics through the journal entry form.
- **View Entries**: Review your past entries and visualize your data through charts.
- **Manage Data**: Export your data for personal analysis or backup purposes.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.