from collections import OrderedDict
import datetime
import time
import sys
import os

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """create the database and the table if they don't exits"""
    db.connect()
    db.create_tables([Entry], safe=True)

def menu_loop():
    """show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quite.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()

def add_entry():
    """add entry"""
    print("Enter your entry. Press ctrls+z and enter when finished.")
    data = sys.stdin.read().strip()
    if data:
        if input('Save entry? [Y/n]').lower() != 'n':
            Entry.create(content=data)
            print("Saved Successfully")

def view_entries(search_query=None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        os.system('cls')
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('='*len(timestamp)+'\n')
        print(entry.content+'\n')
        print('='*len(timestamp)+'\n')
        print('N) for next entry')
        print('q) to return to main menu')
        print('d) to delete entry')

        next_action = input('Action: use  "N" | "d" | "q" ').lower().strip()
        if next_action == 'q':
            os.system('cls')
            break
        elif next_action == 'd':
            delete_entry(entry)
        
def search_entries():
    """Search entries for a string."""
    view_entries(input("Search query: "))

def delete_entry(entry):
    """delete entry"""
    if input("Are your sure? \n [Y/N] \n> ").lower() == 'y':
        entry.delete_instance()
        print("Entry was Deleted!\nMoving to next entry")
        time.sleep(1.5)
    

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
    ('d', delete_entry)
])

if __name__ == '__main__':
    initialize()
    menu_loop()