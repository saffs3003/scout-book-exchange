import numpy as np
import pandas as pd
import ast  
import os
import subprocess

#Book Class
class Book:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Book(id='{self.id}', name='{self.name}')"

# Read Csv Function
def Read_Csv(csv):
    try:
        read = pd.read_csv(csv)
        return read
    except:
        print(f'{csv} is empty, returning Empty DataFrame')
        #returns Empty DataFrame
        return pd.DataFrame()

#Clean CSV Function
def Clean_csv(csv):
    try:
        clean_csv = csv.drop_duplicates().dropna(axis='columns')
        return clean_csv
    except pd.errors.EmptyDataError:
        print(f'{csv} is empty, returning Empty DataFrame')
        return pd.DataFrame()




try:
    #Read Books.csv
   
    books = Read_Csv('BookExchangeDatas/Books.csv')
    books = Clean_csv(books)
    #Setting BookNumber As Index of the Csv
    books.set_index("BookNumber", inplace=True)

    #Read People names
    people = Read_Csv('BookExchangeDatas/People.csv')
    people = Clean_csv(people)




    library = {}
    
    #convert People.csv into a list
    person = people['PersonName'].tolist()


    #Read the Assigned Histroy of a People
    assignedHistory_df = Read_Csv('AssignedHistory.csv')
    print(assignedHistory_df)


    #if Empty make a set for each person
    if assignedHistory_df.empty:
    # Assign books sequentially from books.csv to people.csv
        assignedHistory = {p: [books.index[i]] for i, p in enumerate(person[:len(books)])}


        print(f'Assigned History: {assignedHistory}')
        print(f'Assigned History DF: {assignedHistory_df}')
    else:
    # Convert AssignedBooks string column to list
        assignedHistory = assignedHistory_df.set_index('PersonName')['AssignedBooks'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    ).to_dict()  # Convert the result into a dictionary


    #add books to library
    for book_id in books.index:
        book_name = books.loc[book_id, "BookName"]
        library[book_id] = Book(book_id, book_name)
    
    #check if there are enough Books
    if len(library)<len(person):
        raise MemoryError("Not Enough Books for EveryOne")


    bookAssigned = {}
    
    #so each person gets unique book
    assigned_books_set = set()

    for p in person:
        
        #get assigned_Histroy
        already_assigned_books = assignedHistory.get(p, [])
        
        #check if the book has already been assigned to user before
        #also checks if that book has been assigned to someone this time
        available_books = [book_id for book_id in library if book_id not in assigned_books_set]
        
        
        #if all possible Books has been read/assigned 
        if not available_books:
           # print(f'All possible books combinations reached for {p}. Resetting the assignment history...')
            assignedHistory[p] = []  
            #clear the set
            assigned_books_set.clear()  
            #add the books available for user
            available_books = list(library.keys())  
        
        #random select Id of a book from available _books 
        selected_book_id = np.random.choice(available_books)
        
        #update bookAssigned
        bookAssigned[p] = (library[selected_book_id].name, library[selected_book_id].id)

        #update the Assigned Histroy of user
        assignedHistory[p].append(selected_book_id)
        
        #update assigned_books_set for this run
        assigned_books_set.add(selected_book_id)

        #print(f"Assigned book to {p}: {library[selected_book_id].name} (Book ID: {selected_book_id})")


    #booksAssigned into dict
    data = pd.DataFrame.from_dict(bookAssigned, orient='index', columns=['Book Name', 'Book ID'])
    data.index.name="Name"
    


    #so to convret each book_id is int 
    cleaned_assigned_history = {
        person: [int(book_id) for book_id in book_list]
        for person, book_list in assignedHistory.items()
    }

    assignedHistory_df = pd.DataFrame(list(cleaned_assigned_history.items()), columns=['PersonName', 'AssignedBooks'])

    
    
    BookNames=[]

    #map bookId to Book Names
    for index, row in assignedHistory_df.iterrows():
        Bookids=row['AssignedBooks']
        BookList=[]
        for book in Bookids:
            
            names=library[book].name
            BookList.append(names)
        
        BookNames.append(BookList)

    #create new col
    assignedHistory_df['BookNames'] = BookNames

#add the new col to csv
  
    assignedHistory_df.to_csv("AssignedHistory.csv", index=False)
    data.to_csv("BookAssigned.csv")

    #print("<---completed-->\n")
    AssignedBooks="C:/Users/saffi/OneDrive/Desktop/scout-book-exchange/BookAssigned.csv"
    History="C:/Users/saffi/OneDrive/Desktop/scout-book-exchange/AssignedHistroy.csv"

    #print(f'Assigned Books File : {AssignedBooks} \n')
    #print(f'Histroy of Assigned Books File : {History}\n')

#open excel file
    if os.path.exists(AssignedBooks):
         subprocess.run(['start', 'excel', AssignedBooks], shell=True)
    else:
        print("File:not Found in path {AssignedBooks} path")
 



except Exception as e:
    print(f"Error:Not Possible{e}")

