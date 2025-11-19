import importlib
import inspect
import json
from typing import Dict, List, Tuple
import re

class ParameterSchema:
    """Schema for a single parameter"""
    def __init__(self, name: str, label_expr: str, index: int):
        self.name = name
        self.label_expr = label_expr  # Raw expression from return_state
        self.index = index
        self.value_type = None  # 'numeric', 'category', 'boolean'
        self.categories = []  # For category type
        self.min_value = None  # For numeric type
        self.max_value = None  # For numeric type
        self.display_value_expr = None  # Raw expression for display value
        self.assignment_code = None  # The actual assignment line

class ElementSchema:
    """Complete schema for a generator or effect"""
    def __init__(self, name: str, element_type: str):
        self.name = name
        self.type = element_type
        self.parameters: List[ParameterSchema] = []
        self.version = 1  # Increment on changes

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'version': self.version,
            'parameters': [
                {
                    'index': p.index,
                    'variable_name': p.name,
                    'display_label': p.label_expr,
                    'display_value': p.display_value_expr,
                    'assignment_code': p.assignment_code,
                    'value_type': p.value_type,
                    'categories': p.categories,
                    'min_value': p.min_value,
                    'max_value': p.max_value
                }
                for p in self.parameters
            ]
        }

class SchemaExtractor:
    def __init__(self):
        self.schemas = {}
        self.param_start_marker = "# === PARAMETERS START ==="
        self.param_end_marker = "# === PARAMETERS END ==="
        
    def _parse_return_state(self, source_code: str) -> List[Tuple[str, str, str]]:
        """Parse return_state method to extract parameter info
    
        Returns:
            List of tuples: [(label_expression, variable_name, display_value_expression), ...]
        """
        lines = source_code.split('\n')
        
        # Find the return_state method
        in_return_state = False
        in_return_array = False
        bracket_depth = 0
        return_content = []
        
        for line in lines:
            # Find method definition
            if 'def return_state(self)' in line:
                in_return_state = True
                continue
            
            if not in_return_state:
                continue
            
            # Find the return statement
            if 'return [' in line:
                in_return_array = True
                # Start collecting from this line
                bracket_depth = line.count('[') - line.count(']')
                return_content.append(line)
                
                # Check if it's a single-line return
                if bracket_depth == 0:
                    break
                continue
            
            if in_return_array:
                return_content.append(line)
                bracket_depth += line.count('[') - line.count(']')
                
                # When brackets are balanced, we've reached the end
                if bracket_depth == 0:
                    break
        
        if not return_content:
            raise ValueError("Could not find return statement in return_state()")
        
        # Join the lines and extract the array content
        full_return = ' '.join(return_content)
        
        # Extract everything between the outer 'return [' and final ']'
        match = re.search(r'return\s*\[(.*)\]', full_return, re.DOTALL)
        if not match:
            raise ValueError("Could not parse return array")
        
        array_content = match.group(1)
        
        # Parse individual parameter arrays
        # Each parameter is: [label_expr, 'variable_name', display_value_expr]
        parameters = []
        
        # Split by top-level commas (not within brackets)
        param_strings = self._split_top_level(array_content)
        
        for param_str in param_strings:
            param_str = param_str.strip()
            if not param_str:
                continue
            
            # Parse the parameter array by finding balanced brackets
            # [label_expr, 'variable_name', display_value_expr]
            if not param_str.startswith('['):
                continue
            
            # Extract the three parts by tracking bracket depth
            parts = self._extract_array_elements(param_str)
            
            if len(parts) != 3:
                print(f"      Warning: Expected 3 parts in parameter, got {len(parts)}: {param_str[:50]}...")
                continue
            
            label_expr = parts[0].strip()
            variable_name_expr = parts[1].strip()
            display_value_expr = parts[2].strip()
            
            # Extract variable name (it's always a simple quoted string)
            variable_name = variable_name_expr.strip("'\"")
            
            # Store the raw expressions without modification
            parameters.append((label_expr, variable_name, display_value_expr))
        
        return parameters

    def _extract_array_elements(self, array_str: str) -> List[str]:
        """Extract elements from an array string, respecting nested brackets and parentheses
        
        Args:
            array_str: String like "[elem1, elem2, elem3]"
        
        Returns:
            List of element strings
        """
        # Remove outer brackets
        if array_str.startswith('[') and array_str.endswith(']'):
            inner = array_str[1:-1]
        else:
            inner = array_str
        
        elements = []
        current = []
        depth = 0  # Track bracket/parenthesis depth
        
        for char in inner:
            if char in '[(':
                depth += 1
                current.append(char)
            elif char in '])':
                depth -= 1
                current.append(char)
            elif char == ',' and depth == 0:
                # Top-level comma - this separates elements
                elements.append(''.join(current))
                current = []
            else:
                current.append(char)
        
        # Don't forget the last element
        if current:
            elements.append(''.join(current))
        
        return elements

    def _split_top_level(self, text: str) -> List[str]:
        """Split text by commas, but only at the top bracket level"""
        parts = []
        current = []
        depth = 0
        
        for char in text:
            if char in '[(':
                depth += 1
            elif char in '])':
                depth -= 1
            
            if char == ',' and depth == 0:
                parts.append(''.join(current))
                current = []
            else:
                current.append(char)
        
        if current:
            parts.append(''.join(current))
        
        return parts

    def extract_element_schema(self, element_name: str, element_type: str) -> ElementSchema:
        """Extract complete schema from an element by analyzing its code"""
        
        # Import just to get the source code (no instantiation needed)
        if element_type == 'effect':
            module = importlib.import_module(f'effects.{element_name}')
        else:
            module = importlib.import_module(f'generators.{element_name}')
        
        element_class = getattr(module, element_name)
        
        # Get source code
        source = inspect.getsource(element_class)
        
        schema = ElementSchema(element_name, element_type)
        
        # Parse return_state to get parameter info
        return_state_params = self._parse_return_state(source)
        
        # Parse __call__ to get parameter assignments
        call_source = inspect.getsource(element_class.__call__)
        assignments = self._find_parameter_assignments(call_source)
        
        # Verify counts match
        if len(assignments) != len(return_state_params):
            print(f"    Warning: Found {len(assignments)} assignments but {len(return_state_params)} parameters in return_state")
        
        # Build schema by combining both sources
        for idx, (label_expr, variable_name, display_value_expr) in enumerate(return_state_params):
            param_schema = ParameterSchema(variable_name, label_expr, idx)
            param_schema.display_value_expr = display_value_expr
            
            # Find matching assignment
            if idx < len(assignments):
                assignment_info = assignments[idx]
                param_schema.assignment_code = assignment_info['code']
                
                # Verify names match
                if assignment_info['name'] != variable_name:
                    print(f"    Warning: Parameter name mismatch at index {idx}: "
                          f"assignment='{assignment_info['name']}' vs return_state='{variable_name}'")
            
                # Analyze the assignment to determine type and range
                self._analyze_assignment(param_schema, assignment_info['code'])
            else:
                print(f"    Warning: No assignment found for parameter '{variable_name}' at index {idx}")
            
            schema.parameters.append(param_schema)
        
        return schema
    
    def _find_parameter_assignments(self, source_code: str) -> List[Dict[str, str]]:
        """Find parameter assignments between marker comments"""
        assignments = []
        lines = source_code.split('\n')
        
        in_params_section = False
        
        for line in lines:
            # Check for start marker
            if self.param_start_marker in line:
                in_params_section = True
                continue
            
            # Check for end marker
            if self.param_end_marker in line:
                in_params_section = False
                break
            
            # Extract assignments within the marked section
            if in_params_section:
                match = re.match(r'\s*self\.([^\s=]+)\s*=\s*(.+?)(?:\s*#.*)?$', line)
                if match:
                    param_name = match.group(1)
                    assignment_code = match.group(2).strip()
                    
                    assignments.append({
                        'name': param_name,
                        'code': assignment_code
                    })
        
        return assignments
    
    def _analyze_assignment(self, param: ParameterSchema, assignment_code: str):
        """Analyze assignment code to determine parameter type"""
    
        # Pattern 1: Category - ['cat1', 'cat2', 'cat3'][int(args[x]*N)]
        category_pattern = r'\[([^\]]+)\]\[(?:int\()?(?:round\()?args\[\d+\]\*(\d+\.?\d*)(?:\))?(?:\))?\]'
        category_match = re.search(category_pattern, assignment_code)
        
        if category_match:
            param.value_type = 'category'
            try:
                # Extract the categories list
                categories_str = '[' + category_match.group(1) + ']'
                param.categories = eval(categories_str)
                
                # Validate multiplier
                multiplier = float(category_match.group(2))
                expected_multiplier = len(param.categories) - 1  # For round() usage
                if abs(multiplier - expected_multiplier) > 0.1 and abs(multiplier - len(param.categories)) > 0.1:
                    print(f"      Warning: Category '{param.name}' has {len(param.categories)} items but uses multiplier {multiplier}")
            except Exception as e:
                print(f"      Warning: Failed to parse categories for '{param.name}': {e}")
        
        # Pattern 2: Boolean - args[x] > 0.5 or args[x] < 0.5
        elif '>' in assignment_code or '<' in assignment_code or '==' in assignment_code:
            param.value_type = 'boolean'
            param.min_value = 0
            param.max_value = 1
        
        # Pattern 3: Numeric - args[x] or args[x] * N or args[x] + N
        elif 'args[' in assignment_code:
            param.value_type = 'numeric'
            
            # Clean up code - remove int() wrapper if present
            code = assignment_code
            if code.startswith('int(') and code.endswith(')'):
                code = code[4:-1]
            
            try:
                # Check for multiplication: args[x] * N
                mult_pattern = r'args\[\d+\]\s*\*\s*(\d+\.?\d*)'
                mult_match = re.search(mult_pattern, code)
                
                if mult_match:
                    multiplier = float(mult_match.group(1))
                    
                    # Check if result is cast to int
                    if 'int(' in assignment_code:
                        param.min_value = 0
                        param.max_value = int(multiplier)
                    else:
                        param.min_value = 0.0
                        param.max_value = multiplier
                    
                    # Check for offset
                    if '+' in code and code.index('+') > code.index('*'):
                        offset_match = re.search(r'\+\s*(\d+\.?\d*)', code)
                        if offset_match:
                            offset = float(offset_match.group(1))
                            param.min_value += offset
                            param.max_value += offset
                    elif '-' in code and code.index('-') > code.index('*'):
                        offset_match = re.search(r'-\s*(\d+\.?\d*)', code)
                        if offset_match:
                            offset = float(offset_match.group(1))
                            param.min_value -= offset
                            param.max_value -= offset
                
                # Just args[x] - range is 0.0 to 1.0
                else:
                    param.min_value = 0.0
                    param.max_value = 1.0
                    
            except Exception as e:
                print(f"      Warning: Failed to parse numeric range for '{param.name}': {e}")
                param.min_value = 0.0
                param.max_value = 1.0
    
    def extract_all_schemas(self, output_file: str = 'element_schemas.json'):
        """Extract schemas for all generators and effects"""
        from db_manager import DatabaseManager
        db = DatabaseManager()
        
        generators = db.get_active_elements('generator')
        effects = db.get_active_elements('effect')
        
        all_schemas = {}
        
        print("Extracting generator schemas...")
        for gen in generators:
            try:
                schema = self.extract_element_schema(gen['name'], 'generator')
                all_schemas[f"generator.{gen['name']}"] = schema.to_dict()
                print(f"  ✓ {gen['name']}")
            except Exception as e:
                print(f"  ✗ {gen['name']}: {e}")
        
        print("\nExtracting effect schemas...")
        for eff in effects:
            try:
                schema = self.extract_element_schema(eff['name'], 'effect')
                all_schemas[f"effect.{eff['name']}"] = schema.to_dict()
                print(f"  ✓ {eff['name']}")
            except Exception as e:
                print(f"  ✗ {eff['name']}: {e}")
        
        with open(output_file, 'w') as f:
            json.dump(all_schemas, f, indent=2)
        
        print(f"\n✓ Schemas saved to {output_file}")
        return all_schemas

if __name__ == '__main__':
    extractor = SchemaExtractor()
    extractor.extract_all_schemas()