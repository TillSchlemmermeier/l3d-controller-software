import sqlite3
from contextlib import contextmanager
import json
import os
import numpy as np


class DatabaseManager:
    def __init__(self, db_path: str = 'l3d.db'):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
               
    def init_db(self):
        """Initialize database tables"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS elements (
                    id INTEGER PRIMARY KEY,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
					active INTEGER NOT NULL DEFAULT 1,
                    request_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(type, name)
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS presets (
                    id INTEGER PRIMARY KEY,
                    element_id INTEGER,
                    name TEXT NOT NULL,
                    data TEXT NOT NULL,
                    request_count INTEGER DEFAULT 0,
                	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(element_id) REFERENCES elements(id),
                    UNIQUE(element_id, name)
                );
            ''')
          
            conn.commit()


    def save_preset(self, type: str, element: str, preset: str, data: dict):
        print('save_preset', type, element, preset, data)
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                # Get or create component
                cursor.execute('''
                    INSERT OR IGNORE INTO elements (type, name)
                    VALUES (?, ?)
                ''', (type, element))
                
                cursor.execute('''
                    SELECT id FROM elements
                    WHERE type = ? AND name = ?
                ''', (type, element))
                
                element_id = cursor.fetchone()[0]
                
                cursor.execute('''
                    INSERT OR REPLACE INTO presets (element_id, name, data)
                    VALUES (?, ?, ?)
                ''', (element_id, preset, json.dumps(data, indent=None, separators=(',', ':'))))
                
                conn.commit()
                return True, "Preset saved successfully"
        except Exception as e:
            print(f"Error saving preset: {e}")
            return False


    def convert_string_keys_to_int(self, obj):
        if isinstance(obj, dict):
            return {int(k) if k.isdigit() else k: self.convert_string_keys_to_int(v) 
                    for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_string_keys_to_int(elem) for elem in obj]
        return obj
    

    def get_preset(self, type: str, element: str, preset: str, increment_count: bool = True):
        """Get any preset with a single method"""
        if type == 'global' or type == 'channel':
            element = 'presets'
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.data
                FROM presets p
                JOIN elements c ON p.element_id = c.id
                WHERE c.type = ? AND c.name = ? AND p.name = ?
            ''', (type, element, preset))
            row = cursor.fetchone()
            if increment_count:
                self.increment_request_count(type, element, preset)
            if row:
                data = json.loads(row[0])
                return self.convert_string_keys_to_int(data)
            return None


    def get_element_names(self, type: str):
        """Get all elements of a type with their metadata"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    name,
                    active
                FROM elements 
                WHERE type = ?
                ORDER BY name
            ''', (type,))
            
            return [
                {
                    'name': row[0],
                    'active': bool(row[1]),
                }
                for row in cursor.fetchall()
            ]


    def get_preset_names(self, type: str, element: str):
        """Get all preset names for a specific element"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.name,
                    strftime('%Y-%m-%d %H:%M:%S', p.created_at) as created_at,
                    p.request_count
                FROM presets p
                JOIN elements c ON p.element_id = c.id
                WHERE c.type = ? AND c.name = ?
                ORDER BY p.request_count DESC
            ''', (type, element))
            
            return [
                {
                    'name': row[0],
                    'created_at': row[1],
                    'request_count': row[2]
                }
                for row in cursor.fetchall()
            ]
    
    
    def get_active_elements(self, type: str) -> list:
        """Get all active elements of a specific type"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    name,
                    strftime('%Y-%m-%d %H:%M:%S', created_at) as created_at,
                    request_count
                FROM elements 
                WHERE type = ? AND active = 1
            ''', (type,))
            return [
                {
                    'name': row[0],
                    'created_at': row[1],
                    'request_count': row[2]
                }
                for row in cursor.fetchall()
            ]
    

    def increment_request_count(self, type: str, element: str, preset: str):
        """Increment the load count for a preset"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()

                # Update preset request count
                cursor.execute('''
                    UPDATE presets 
                    SET request_count = request_count + 1
                    WHERE id IN (
                        SELECT p.id
                        FROM presets p
                        JOIN elements e ON p.element_id = e.id
                        WHERE e.type = ? AND e.name = ? AND p.name = ?
                    )
                ''', (type, element, preset))

                # Update element request count
                cursor.execute('''
                    UPDATE elements
                    SET request_count = request_count + 1
                    WHERE type = ? AND name = ?
                ''', (type, element))

                conn.commit()
        except Exception as e:
            print(f"Error incrementing load count: {e}")


    def rename_preset(self, type: str, element: str, old_name: str, new_name: str) -> bool:
        """Rename a preset"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE presets 
                    SET name = ?
                    WHERE id IN (
                        SELECT p.id
                        FROM presets p
                        JOIN elements e ON p.element_id = e.id
                        WHERE e.type = ? AND e.name = ? AND p.name = ?
                    )
                ''', (new_name, type, element, old_name))
                
                db_success = cursor.rowcount > 0
                conn.commit()
                
                return db_success

        except Exception as e:
            print(f"Error renaming preset: {e}")
            return False
            

    def delete_preset(self, type: str, element: str, preset: str) -> bool:
        """Delete a preset
        Returns bool: True if preset was deleted, False if error or not found
        """
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Delete preset using JOIN to ensure element type/name match
                cursor.execute('''
                    DELETE FROM presets 
                    WHERE id IN (
                        SELECT p.id
                        FROM presets p
                        JOIN elements e ON p.element_id = e.id
                        WHERE e.type = ? AND e.name = ? AND p.name = ?
                    )
                ''', (type, element, preset))
                
                db_success = cursor.rowcount > 0
                conn.commit()
                
                # If preset was found and deleted from DB, try to delete the GIF
                if db_success:
                    gif_path = f"../src/assets/previews/{element}_p_{preset}.gif"
                    try:
                        if os.path.exists(gif_path):
                            os.remove(gif_path)
                    except OSError as e:
                        print(f"Warning: Could not delete GIF file: {e}")
                        # Don't return False here as the DB deletion was successful
            
                return db_success

        except Exception as e:
            print(f"Error deleting preset: {e}")
            return False
        
    def delete_element(self, type: str, element: str) -> bool:
        """Delete an element and all its associated presets
        Returns bool: True if element was deleted, False if error or not found
        """
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Get all associated presets
                cursor.execute('''
                    SELECT p.name
                    FROM presets p
                    JOIN elements e ON p.element_id = e.id
                    WHERE e.type = ? AND e.name = ?
                ''', (type, element))
                
                # Delete each preset and associated GIF file
                presets = [row[0] for row in cursor.fetchall()]
                for preset in presets:
                    self.delete_preset(type, element, preset)
                
                # Delete the element itself
                cursor.execute('''
                    DELETE FROM elements 
                    WHERE type = ? AND name = ?
                ''', (type, element))
                
                success = cursor.rowcount > 0
                conn.commit()
                       
                return success
                
        except Exception as e:
            print(f"Error deleting element: {e}")
            return False


    def toggle_element_active(self, type: str, name: str) -> bool:
        """Toggle the active status of an element
        Returns bool: True if status was toggled, False if error or not found
        """
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Toggle active status
                cursor.execute('''
                    UPDATE elements
                    SET active = CASE 
                        WHEN active = 1 THEN 0 
                        ELSE 1 
                    END
                    WHERE type = ? AND name = ?
                    RETURNING active
                ''', (type, name))
                
                result = cursor.fetchone()
                if result:
                    conn.commit()
                    return True
                return False
        
        except Exception as e:
            print(f"Error toggling element status: {e}")
            return False


    def preset_exists(self, type: str, element: str, preset: str) -> bool:
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*)
                FROM presets p
                JOIN elements e ON p.element_id = e.id
                WHERE e.type = ? AND e.name = ? AND p.name = ?
            ''', (type, element, preset))
            return cursor.fetchone()[0] > 0


    def get_element_info(self, type: str, name: str) -> dict:
        """Get all available information for a specific element."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    name,
                    type,
                    active,
                    request_count,
                    strftime('%Y-%m-%d %H:%M:%S', created_at) as created_at
                FROM elements
                WHERE type = ? AND name = ?
            ''', (type, name))
            
            row = cursor.fetchone()
            if row:
                return {
                    'name': row[0],
                    'type': row[1],
                    'isActive': bool(row[2]),
                    'usageCount': row[3],
                    'created': row[4]
                }
            return None

    def get_preset_info(self, type: str, element: str, preset: str) -> dict:
        """Get all available information for a specific preset."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.name,
                    e.name as element_name,
                    p.data,
                    p.request_count,
                    strftime('%Y-%m-%d %H:%M:%S', p.created_at) as created_at
                FROM presets p
                JOIN elements e ON p.element_id = e.id
                WHERE e.type = ? AND e.name = ? AND p.name = ?
            ''', (type, element, preset))
            
            row = cursor.fetchone()
            if row:
                return {
                    'name': row[0],
                    'elementName': row[1],
                    'data': json.loads(row[2]),
                    'usageCount': row[3],
                    'created': row[4]
                }
            return None


    def add_element(self, type: str, name: str) -> bool:
        """Add a new generator or effect to the database with a basic preset
        Returns bool: True if element was added successfully"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                try:
                    # Insert new element
                    cursor.execute('''
                        INSERT INTO elements (type, name)
                        VALUES (?, ?)
                    ''', (type, name))
                    
                    element_id = cursor.lastrowid
                    
                    # Create a local namespace for exec
                    namespace = {}

                    # Import the module into our namespace
                    exec(f'from {type}s.{name} import *', namespace)

                    # Initialize element in the namespace
                    exec(f'element = {name}()', namespace)
                    
                    # Get the element from namespace
                    element = namespace['element']
                    
                    # Call element with appropriate arguments
                    if type == 'generator':
                        element([0, 0, 0, 0, 0, 0, 0, 0])
                    elif type == 'effect':
                        dummy_world = np.zeros([3, 10, 10, 10])
                        element(dummy_world, [0, 0, 0, 0, 0, 0, 0, 0])
                    
                    # Get state and format params
                    state = element.return_state()
                    params = []
                    for param in state:
                        params.extend([param[0], param[1], param[2], 0])
                    
                    # Create and save basic preset
                    preset_data = {
                        "name": name,
                        "update": 1,
                        "params": params
                    }

                    if type == 'effect':
                        preset_data['IO'] = 1
                    
                    cursor.execute('''
                        INSERT INTO presets (element_id, name, data)
                        VALUES (?, 'basic', ?)
                    ''', (element_id, json.dumps(preset_data)))
                    
                    conn.commit()
                    print(f"Element and basic preset added successfully")
                    return True
                    
                except Exception as e:
                    print(f"Error creating element or preset: {e}")
                    conn.rollback()  # Rollback the entire transaction
                    return False
                    
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False