import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('terminals.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS terminals (
        id INTEGER PRIMARY KEY,
        status TEXT,
        terminal TEXT,
        satellite TEXT,
        state TEXT,
        city TEXT,
        address TEXT,
        zip_code TEXT,
        regional_manager TEXT,
        terminal_manager TEXT
    )
''')


def create_terminal(status, terminal, satellite, state, city, address, zip_code, regional_manager, terminal_manager):
    cursor.execute('''
        INSERT INTO terminals (status, terminal, satellite, state, city, address, zip_code, regional_manager, terminal_manager)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (status, terminal, satellite, state, city, address, zip_code, regional_manager, terminal_manager))
    conn.commit()


def get_terminals():
    cursor.execute('SELECT * FROM terminals')
    return cursor.fetchall()


def update_terminal(id, status, terminal, satellite, state, city, address, zip_code, regional_manager, terminal_manager):
    cursor.execute('''
        UPDATE terminals
        SET status=?, terminal=?, satellite=?, state=?, city=?, address=?, zip_code=?, regional_manager=?, terminal_manager=?
        WHERE id=?
    ''', (status, terminal, satellite, state, city, address, zip_code, regional_manager, terminal_manager, id))
    conn.commit()


def delete_terminal(id):
    cursor.execute('DELETE FROM terminals WHERE id=?', (id,))
    conn.commit()

st.title('Terminal CRUD App')

# Create Terminal
st.header('Create Terminal')
status = st.text_input('Status')
terminal = st.text_input('Terminal')
satellite = st.text_input('Satellite')
state = st.text_input('State')
city = st.text_input('City')
address = st.text_input('Address')
zip_code = st.text_input('Zip Code')
regional_manager = st.text_input('Regional Manager')
terminal_manager = st.text_input('Terminal Manager')

if st.button('Create'):
    create_terminal(status, terminal, satellite, state, city, address, zip_code, regional_manager, terminal_manager)
    st.success('Terminal created successfully!')

# List Terminals
st.header('List Terminals')
terminals=get_terminals()
for term in terminals:
    st.write(f"ID: {term[0]}, Terminal: {term[2]}, Status: {term[1]}")

# Update Terminal
st.header('Update Terminal')
update_id = st.number_input('Enter ID of the terminal to update:')
if update_id > 0:
    update_status = st.text_input('Status')
    update_terminal_name = st.text_input('Terminal')
    update_satellite = st.text_input('Satellite')
    update_state = st.text_input('State')
    update_city = st.text_input('City')
    update_address = st.text_input('Address')
    update_zip_code = st.text_input('Zip Code')
    update_regional_manager = st.text_input('Regional Manager')
    update_terminal_manager = st.text_input('Terminal Manager')

    if st.button('Update'):
        update_terminal(update_id, update_status, update_terminal_name, update_satellite, update_state, update_city,
                        update_address, update_zip_code, update_regional_manager, update_terminal_manager)
        st.success('Terminal updated successfully!')

# Delete Terminal
st.header('Delete Terminal')
delete_id = st.number_input('Enter ID of the terminal to delete:')
if st.button('Delete'):
    delete_terminal(delete_id)
    st.success('Terminal deleted successfully!')

# Close the database connection
conn.close()



