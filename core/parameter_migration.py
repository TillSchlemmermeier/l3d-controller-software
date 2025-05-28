from typing import List, Dict, Union, Callable
from preset_updater import update_presets

class ParameterMigration:
    @staticmethod
    def add_category(params: List, param_index: int, new_value: str) -> List:
        """
        Add new category to parameter's possible values
        Example: Adding 'Medium' to size categories ['Small', 'Large']
        """
        return params  # Original params unchanged, just documents the change

    @staticmethod
    def remove_category(params: List, param_index: int, old_value: str, fallback_value: str) -> List:
        """
        Remove a category and replace with fallback
        Example: Removing 'Medium' size, fallback to 'Small'
        """
        if params[param_index] == old_value:
            params[param_index] = fallback_value
        return params

    @staticmethod
    def rename_category(params: List, param_index: int, old_name: str, new_name: str) -> List:
        """
        Rename a category
        Example: Rename 'Trigger' to 'OneShot' in channel parameter
        """
        if params[param_index] == old_name:
            params[param_index] = new_name
        return params

    @staticmethod
    def extend_range(params: List, param_index: int, old_max: float, new_max: float) -> List:
        """
        Extend the range of a parameter
        Example: Change speed range from 0-10 to 0-20
        """
        if isinstance(params[param_index], (int, float)):
            params[param_index] = params[param_index] * (new_max/old_max)
        return params

    @staticmethod
    def shrink_range(params: List, param_index: int, old_max: float, new_max: float) -> List:
        """
        Shrink the range of a parameter
        Example: Change size range from 0-10 to 0-5
        """
        if isinstance(params[param_index], (int, float)):
            params[param_index] = params[param_index] * (new_max/old_max)
        return params

    @staticmethod
    def add_parameter(params: List, name: str, type_: str, default_value: Union[str, float], 
                     midi_value: float) -> List:
        """
        Add a new parameter with default values
        Example: Add new 'rotation' parameter
        """
        params.extend([name, type_, default_value, midi_value])
        return params

    @staticmethod
    def remove_parameter(params: List, param_index: int) -> List:
        """
        Remove a parameter and its associated values
        Example: Remove deprecated 'glow' parameter
        """
        del params[param_index:param_index+4]
        return params

    @staticmethod
    def rename_parameter(params: List, param_index: int, new_name: str) -> List:
        """
        Rename a parameter
        Example: Rename 'size' to 'scale'
        """
        params[param_index] = new_name
        return params

    @staticmethod
    def reorder_parameters(params: List, new_order: List[int]) -> List:
        """
        Reorder parameters
        Example: Move 'speed' parameter to front
        """
        new_params = []
        for i in new_order:
            new_params.extend(params[i*4:(i+1)*4])
        return new_params

# Example migrations:

def migrate_g_cube_v1_to_v2():
    """Example migration for g_cube from v1 to v2"""
    def update_func(params: List) -> List:
        # Add new 'rotation' parameter
        params = ParameterMigration.add_parameter(
            params, 
            "rotation", 
            "speed", 
            0.0,  # default value 
            0.5   # default midi value
        )
        
        # Rename 'size' to 'scale'
        params = ParameterMigration.rename_parameter(params, 0, "scale")
        
        # Extend speed range
        speed_index = 12  # assuming speed is 4th parameter
        params = ParameterMigration.extend_range(params, speed_index, 10, 20)
        
        return params
    
    update_presets('g_cube', 'generator', update_func)

def migrate_e_rainbow_v2_to_v3():
    """Example migration for e_rainbow from v2 to v3"""
    def update_func(params: List) -> List:
        # Remove old 'glow' parameter (was 2nd parameter)
        params = ParameterMigration.remove_parameter(params, 4)
        
        # Add new categories to channel parameter
        params = ParameterMigration.add_category(params, 8, "Mix")
        
        # Shrink speed range
        params = ParameterMigration.shrink_range(params, 2, 1.0, 0.5)
        
        return params
    
    update_presets('e_rainbow', 'effect', update_func)


    # Example of combining multiple migrations
def migrate_g_cube_v2_to_v3():
    def update_func(params: List) -> List:
        # 1. Add new parameter
        params = ParameterMigration.add_parameter(
            params, "brightness", "amount", 1.0, 0.8
        )
        
        # 2. Change channel categories
        if params[8] == "Trigger":  # Assuming channel is 3rd parameter
            params = ParameterMigration.rename_category(
                params, 8, "Trigger", "OneShot"
            )
        
        # 3. Reorder parameters to put brightness first
        num_params = len(params) // 4
        new_order = [num_params-1] + list(range(num_params-1))
        params = ParameterMigration.reorder_parameters(params, new_order)
        
        return params
    
    update_presets('g_cube', 'generator', update_func)