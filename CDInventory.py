#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File.
# Kenny Lu, 2020-Feb-29, Initial Commit. 
# DKlos, 2020-Mar-02, Refactored code, grading.
# Kenny Lu, 2020-Mar-06, Added Structured error handling.
# Kenny Lu, 2020-Mar-08, Added pickling for read/write.
# Kenny Lu, 2020-Mar-09, Updated docstrings. 
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
binFileName = 'CDInventory.dat' # binary storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    """Handling data processing adding and deleting data"""
    
    @staticmethod
    def add_item(cd_id, cd_title, cd_artist, table):
        """Add data processing to list of dicts data structure.
    
        Args:
            cd_id (integer): ID of the data entry
            cd_title (string): name of CD title
            cd_artist (string): name of the artist

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        """
        new_cd = {'ID': cd_id, 'Title': cd_title, 'Artist': cd_artist}
        table.append(new_cd)
        print("\n""CD Title:", new_cd['Title'], "has been added.""\n")
        return table
      
    @staticmethod
    def delete_item(cd_id, table):
        """Delete data from list of dicts data structure.

        Args:
            cd_id (int): ID of the data entry
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == cd_id:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed.')
        else:
            print('Could not find this CD!')

        return table

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Unpickle the data from binary file identified by file_name

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        """
        # Try-except to not crash the program if target file doesn't exist
        try: 
            with open(binFileName, 'rb') as fileObj:
                table = pickle.load(fileObj)
        except FileNotFoundError:
            print("The file {} could not be loaded".format(file_name))
        
        return table


    @staticmethod
    def write_file(file_name, table):
    # def write_file(file_name, table):
        """Function to write data in memory to file

        Pickle the data from memory and write to a binary data storage file
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """   
        # Try-except to not crash the program if target file cannot be written or saved 
        try:
            with open(binFileName, "wb") as fileObj:
               pickle.dump(lstTbl, fileObj)
        except IOError as e:      
            print("ERROR: The file {} could not be written or saved. Returning to the menu.".format(file_name) + '\n') 

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def add_data():
        """Get data from user to be added into list of dicts data structure.

        Args:
            None.

        Returns:
            cd_id (integer): ID of the new CD
            cd_title (string): Title of the new CD
            cd_artist (string): Artist of the new CD

        """
        while True:
            str_cd_id = input('Enter ID (Integer only): ').strip()
            # Allow user to input 'exit' to get out of the loop
            if str_cd_id.lower() == 'exit':
                break
            # Try-except to ensure input is integer
            try:
                cd_id = int(str_cd_id) 
            except ValueError as e:
                print("Oops! Please enter integer only. Try again or type \'exit\' to return to the menu.")  
                continue
            cd_title = input('What is the CD\'s title? ').strip()
            cd_artist = input('What is the Artist\'s name? ').strip()
            return cd_id, cd_title, cd_artist
       
# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(binFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(binFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # 3.3.2 Add item to the table
        # Try-except in case user wants to exit out of the loop
        try:
            lstTbl = DataProcessor.add_item(*IO.add_data(), lstTbl)
        except Exception as e:
            print("Returning to the menu...")           
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        # Check if inventory is empty, no need to delete if there's nothing in inventory
        if len(lstTbl) != 0: 
            strIDDel = input('Which ID would you like to delete (Integer only)? ').strip()
        # 3.5.2 search thru table and delete CD
        # Try-except to ensure input is integer
            try: 
                intIDDel = int(strIDDel)
            except ValueError as e:
                print("Please enter integer only!")  
                continue
            lstTbl = DataProcessor.delete_item(intIDDel, lstTbl)
        else:
            print("Sorry nothing to delete empty inventory." '\n')
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(binFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')
