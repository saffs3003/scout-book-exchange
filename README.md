# Book Exchange Assignment System

This project automates the assignment of books to a list of people from a predefined library, ensuring no one receives the same book more than once. It also tracks the assignment history.

## Features

- Random book assignment to people
- Tracks book assignment history
- Handles missing or empty CSV files

## Requirements

- **pandas**: For handling CSV data
- **numpy**: For random selection of books

## Install the required libraries:
pip install pandas numpy
or
pip install -r requirements.txt


## File Structure
/BookExchangeDatas
    Books.csv            # List of books with columns BookNumber and BookName
    People.csv           # List of people with a PersonName column
AssignedHistory.csv     # Tracks historical book assignments
BookAssigned.csv        # Final book assignments

## Setup
Clone the project and place Books.csv, People.csv, and AssignedHistory.csv in the /BookExchangeDatas folder.
Run the script using Python:
python Book-exchange.py

## How it Works
The script reads Books.csv and People.csv.
It randomly assigns unique books to each person.
It updates AssignedHistory.csv and creates BookAssigned.csv to store the assignments.
