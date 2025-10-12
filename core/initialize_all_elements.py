from core.db_manager import DatabaseManager
import argparse
import importlib.util
import json
from pathlib import Path
from multiprocessing import shared_memory
import numpy as np

def create_mock_s2l_memory():
    """Create temporary shared memory for initialization"""
    try:
        # Try to access existing shared memory
        shm = shared_memory.SharedMemory(name="global_s2l_memory")
    except FileNotFoundError:
        # Create mock data: 10 channels, 8 bytes each, initialized with '0.0'
        mock_data = bytearray()
        for _ in range(10):
            mock_data.extend("0.0".ljust(8).encode('utf-8'))
        
        shm = shared_memory.SharedMemory(
            name="global_s2l_memory",
            create=True,
            size=len(mock_data)
        )
        shm.buf[:] = mock_data
    return shm

def cleanup_mock_s2l_memory(shm):
    """Clean up temporary shared memory"""
    shm.close()
    try:
        shm.unlink()
    except Exception:
        pass
    

def load_generator_class(name: str):
    """Dynamically load a generator class from the generators folder"""
    try:
        # Construct path to generator file
        file_path = Path(__file__).parent / 'effects' / f'{name}.py'
        
        # Load module
        spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get class from module (assuming class name matches file name)
        return getattr(module, name)
    except Exception as e:
        print(f"Error loading generator {name}: {e}")
        return None

def create_basic_preset(element_name: str, element_type: str) -> dict:
    """Create basic preset data for a generator or effect
    
    Args:
        element_name: Name of the generator/effect
        element_type: Either 'generator' or 'effect'
    """
    try:
        # Load and instantiate element
        element_class = load_generator_class(element_name)
        if not element_class:
            return None
            
        element = element_class()
        
        # Call element with appropriate arguments
        if element_type == 'generator':
            element([0, 0, 0, 0])
        elif element_type == 'effect':
            # Create dummy world array for effect initialization
            import numpy as np
            dummy_world = np.zeros([3, 10, 10, 10])
            element(dummy_world, [0, 0, 0, 0])
        
        # Get state and format params
        state = element.return_state()
        params = []
        for param in state:
            params.extend([param[0], param[1], param[2], 0])
        
        # Create preset data
        preset_data = {
            "name": element_name,
            "IO": 1,
            "update": 1,
            "params": params
        }
        
        return preset_data
    except Exception as e:
        print(f"Error creating basic preset for {element_name}: {e}")
        return None
    

def init_elements():
    """Initialize all generators from generators.dat with basic presets"""
    db = DatabaseManager()
    shm = create_mock_s2l_memory()
    
    # Read generators from file
    with open('effects.dat', 'r') as f:
        effects = [line.strip() for line in f if line.strip()]
    
    try:
        with db.get_db_connection() as conn:
            cursor = conn.cursor()
            
            for effect_name in effects:
                # Insert generator into elements
                cursor.execute('''
                    INSERT OR IGNORE INTO elements (type, name)
                    VALUES (?, ?)
                ''', ('effect', effect_name))
                
                # Get the element_id
                cursor.execute('SELECT id FROM elements WHERE type = ? AND name = ?',
                             ('effect', effect_name))
                element_id = cursor.fetchone()[0]
                
                # Create basic preset data
                preset_data = create_basic_preset(effect_name, 'effect')
                if preset_data:
                    # Store in database
                    cursor.execute('''
                        INSERT OR REPLACE INTO presets (element_id, name, data)
                        VALUES (?, 'basic', ?)
                    ''', (element_id, json.dumps(preset_data)))
                
            conn.commit()
            print(f"Successfully initialized {len(effects)} effects")
    
    except Exception as e:
        print(f"Error initializing effects: {e}")

    finally:
        cleanup_mock_s2l_memory(shm)
if __name__ == "__main__":
    init_elements()