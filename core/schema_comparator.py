import json
import os
from typing import Dict, List, Optional
from enum import Enum
from pathlib import Path

class ChangeType(Enum):
    PARAM_ADDED = "parameter_added"
    PARAM_REMOVED = "parameter_removed"
    PARAM_RENAMED = "parameter_renamed"
    ASSIGNMENT_CHANGED = "assignment_changed"
    LABEL_EXPR_CHANGED = "label_expression_changed"
    DISPLAY_VALUE_EXPR_CHANGED = "display_value_expression_changed"
    RANGE_CHANGED = "range_changed"
    CATEGORIES_CHANGED = "categories_changed"
    TYPE_CHANGED = "type_changed"
    ELEMENT_ADDED = "element_added"
    ELEMENT_REMOVED = "element_removed"

class SchemaChange:
    def __init__(self, element_name: str, element_type: str, change_type: ChangeType):
        self.element_name = element_name
        self.element_type = element_type
        self.change_type = change_type
        self.details = {}
    
    def __repr__(self):
        details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
        return f"{self.element_type}.{self.element_name}: {self.change_type.value} ({details_str})"
    
    def requires_migration(self) -> bool:
        """Returns True if this change requires preset migration"""
        # Changes that affect preset data structure
        migration_required = [
            ChangeType.PARAM_ADDED,
            ChangeType.PARAM_REMOVED,
            ChangeType.PARAM_RENAMED,
            ChangeType.RANGE_CHANGED,
            ChangeType.CATEGORIES_CHANGED,
            ChangeType.TYPE_CHANGED,
            ChangeType.ASSIGNMENT_CHANGED
        ]
        return self.change_type in migration_required

class SchemaComparator:
    def __init__(self, schema_file: str = 'element_schemas.json'):
        """
        Initialize the comparator
        
        Args:
            schema_file: Path to the schema file (will be loaded as old, and updated with new)
        """
        self.schema_file = Path(schema_file)
        self.old_schemas = {}
        self.new_schemas = {}
        
        # Load old schema if it exists
        if self.schema_file.exists():
            with open(self.schema_file) as f:
                self.old_schemas = json.load(f)
            print(f"Loaded existing schema from {self.schema_file}")
        else:
            print(f"No existing schema found at {self.schema_file}")
            print("This will create the initial schema file.")
    
    def extract_current_schema(self) -> Dict:
        """Extract current schema from code"""
        # Import here to avoid circular dependencies
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from schema_extractor import SchemaExtractor
        
        print("\n" + "="*70)
        print("EXTRACTING CURRENT SCHEMA FROM CODE")
        print("="*70 + "\n")
        
        extractor = SchemaExtractor()
        # Extract to temp location first
        temp_file = self.schema_file.parent / 'temp_schema.json'
        self.new_schemas = extractor.extract_all_schemas(str(temp_file))
        
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()
        
        return self.new_schemas
    
    def compare_all(self) -> List[SchemaChange]:
        """Compare all schemas and return list of changes"""
        changes = []
        
        if not self.old_schemas:
            # First time running - no comparison needed
            return changes
        
        all_elements = set(self.old_schemas.keys()) | set(self.new_schemas.keys())
        
        for element_key in sorted(all_elements):
            # Element removed
            if element_key not in self.new_schemas:
                element_type, element_name = element_key.split('.', 1)
                change = SchemaChange(element_name, element_type, ChangeType.ELEMENT_REMOVED)
                change.details = {'message': 'Element no longer exists in code'}
                changes.append(change)
                continue
            
            # Element added
            if element_key not in self.old_schemas:
                new_schema = self.new_schemas[element_key]
                change = SchemaChange(new_schema['name'], new_schema['type'], ChangeType.ELEMENT_ADDED)
                change.details = {
                    'message': 'New element detected',
                    'param_count': len(new_schema['parameters'])
                }
                changes.append(change)
                continue
            
            # Compare existing element
            element_changes = self._compare_element(
                self.old_schemas[element_key],
                self.new_schemas[element_key]
            )
            changes.extend(element_changes)
        
        return changes
    
    def _compare_element(self, old_schema: Dict, new_schema: Dict) -> List[SchemaChange]:
        """Compare two element schemas in detail"""
        changes = []
        element_name = new_schema['name']
        element_type = new_schema['type']
        
        old_params = {p['index']: p for p in old_schema['parameters']}
        new_params = {p['index']: p for p in new_schema['parameters']}
        
        # Check for added parameters
        for idx, new_param in new_params.items():
            if idx not in old_params:
                change = SchemaChange(element_name, element_type, ChangeType.PARAM_ADDED)
                change.details = {
                    'param_index': idx,
                    'param_name': new_param['variable_name'],
                    'param_label': new_param['display_label'],
                    'value_type': new_param['value_type'],
                    'categories': new_param.get('categories', []),
                    'min_value': new_param.get('min_value'),
                    'max_value': new_param.get('max_value')
                }
                changes.append(change)
        
        # Check for removed parameters
        for idx, old_param in old_params.items():
            if idx not in new_params:
                change = SchemaChange(element_name, element_type, ChangeType.PARAM_REMOVED)
                change.details = {
                    'param_index': idx,
                    'param_name': old_param['variable_name'],
                    'param_label': old_param['display_label']
                }
                changes.append(change)
        
        # Check for parameter changes (both exist at same index)
        for idx in sorted(set(old_params.keys()) & set(new_params.keys())):
            old_param = old_params[idx]
            new_param = new_params[idx]
            
            # Variable name changed
            if old_param['variable_name'] != new_param['variable_name']:
                change = SchemaChange(element_name, element_type, ChangeType.PARAM_RENAMED)
                change.details = {
                    'param_index': idx,
                    'old_name': old_param['variable_name'],
                    'new_name': new_param['variable_name']
                }
                changes.append(change)
            
            # Display label expression changed
            if old_param['display_label'] != new_param['display_label']:
                change = SchemaChange(element_name, element_type, ChangeType.LABEL_EXPR_CHANGED)
                change.details = {
                    'param_index': idx,
                    'param_name': new_param['variable_name'],
                    'old_expr': old_param['display_label'],
                    'new_expr': new_param['display_label']
                }
                changes.append(change)
            
            # Display value expression changed
            if old_param.get('display_value') != new_param.get('display_value'):
                change = SchemaChange(element_name, element_type, ChangeType.DISPLAY_VALUE_EXPR_CHANGED)
                change.details = {
                    'param_index': idx,
                    'param_name': new_param['variable_name'],
                    'old_expr': old_param.get('display_value'),
                    'new_expr': new_param.get('display_value')
                }
                changes.append(change)
            
            # Assignment code changed
            if old_param.get('assignment_code') != new_param.get('assignment_code'):
                change = SchemaChange(element_name, element_type, ChangeType.ASSIGNMENT_CHANGED)
                change.details = {
                    'param_index': idx,
                    'param_name': new_param['variable_name'],
                    'old_assignment': old_param.get('assignment_code'),
                    'new_assignment': new_param.get('assignment_code')
                }
                changes.append(change)
            
            # Type changed
            if old_param.get('value_type') != new_param.get('value_type'):
                change = SchemaChange(element_name, element_type, ChangeType.TYPE_CHANGED)
                change.details = {
                    'param_index': idx,
                    'param_name': new_param['variable_name'],
                    'old_type': old_param.get('value_type'),
                    'new_type': new_param.get('value_type')
                }
                changes.append(change)
            
            # Range changed (for numeric types)
            if (new_param.get('value_type') == 'numeric' and
                (old_param.get('min_value') != new_param.get('min_value') or
                 old_param.get('max_value') != new_param.get('max_value'))):
                change = SchemaChange(element_name, element_type, ChangeType.RANGE_CHANGED)
                change.details = {
                    'param_index': idx,
                    'param_name': new_param['variable_name'],
                    'old_min': old_param.get('min_value'),
                    'old_max': old_param.get('max_value'),
                    'new_min': new_param.get('min_value'),
                    'new_max': new_param.get('max_value')
                }
                changes.append(change)
            
            # Categories changed (for category types)
            if (new_param.get('value_type') == 'category' and
                old_param.get('categories') != new_param.get('categories')):
                change = SchemaChange(element_name, element_type, ChangeType.CATEGORIES_CHANGED)
                change.details = {
                    'param_index': idx,
                    'param_name': new_param['variable_name'],
                    'old_categories': old_param.get('categories', []),
                    'new_categories': new_param.get('categories', [])
                }
                changes.append(change)
        
        return changes
    
    def save_new_schema(self):
        """Save the new schema to file, replacing the old one"""
        with open(self.schema_file, 'w') as f:
            json.dump(self.new_schemas, f, indent=2)
        
        print(f"\n✓ Schema saved to {self.schema_file}")
    
    def _print_changes(self, changes: List[SchemaChange]):
        """Pretty print changes grouped by element"""
        if not changes:
            return
        
        # Group changes by element for better readability
        changes_by_element = {}
        for change in changes:
            key = f"{change.element_type}.{change.element_name}"
            if key not in changes_by_element:
                changes_by_element[key] = []
            changes_by_element[key].append(change)
        
        print(f"\n{'='*70}")
        print(f"DETECTED {len(changes)} CHANGE(S)")
        print(f"{'='*70}")
        
        for element_key, element_changes in sorted(changes_by_element.items()):
            print(f"\n{element_key}:")
            for change in element_changes:
                print(f"  • {change.change_type.value}")
                for key, value in change.details.items():
                    # Truncate long values
                    val_str = str(value)
                    if len(val_str) > 60:
                        val_str = val_str[:57] + "..."
                    print(f"      {key}: {val_str}")
    
    def run_workflow(self):
        """Main workflow: extract, compare, migrate (if needed), and save"""
        print("\n" + "="*70)
        print("SCHEMA MANAGEMENT WORKFLOW")
        print("="*70)
        
        # Step 1: Extract current schema from code
        self.extract_current_schema()
        
        # Step 2: Compare with previous schema
        print("\n" + "="*70)
        print("COMPARING WITH PREVIOUS SCHEMA")
        print("="*70)
        
        changes = self.compare_all()
        
        # Step 3: Handle changes
        if not changes:
            print("\n✓ No changes detected!")
            print("Updating schema file with current extraction...")
            self.save_new_schema()
            print("\nWorkflow complete.")
            return
        
        # Print changes
        self._print_changes(changes)
        
        # Separate migration-required changes from cosmetic changes
        migration_changes = [c for c in changes if c.requires_migration()]
        cosmetic_changes = [c for c in changes if not c.requires_migration()]
        
        print(f"\n{'='*70}")
        print(f"MIGRATION ANALYSIS")
        print(f"{'='*70}")
        print(f"Changes requiring migration: {len(migration_changes)}")
        print(f"Cosmetic changes only: {len(cosmetic_changes)}")
        
        if migration_changes:
            print("\n⚠ MIGRATION REQUIRED")
            print("The following changes affect preset data structure:")
            for change in migration_changes:
                print(f"  • {change}")
            
            print("\n" + "="*70)
            print("OPTIONS")
            print("="*70)
            print("1. Run schema_migrator to handle conflicts (recommended)")
            print("2. Save schema without migration (DANGEROUS - may break presets)")
            print("3. Cancel (keep old schema)")
            
            while True:
                choice = input("\nYour choice (1-3): ").strip()
                
                if choice == '1':
                    print("\n" + "="*70)
                    print("MIGRATION WORKFLOW")
                    print("="*70)
                    print("Please run the schema_migrator script to handle these conflicts:")
                    print(f"  python -m core.preset_administration.schema_migrator")
                    print("\nThe migrator will prompt you for each conflict.")
                    print("After migration is complete, the schema will be automatically saved.")
                    print("\nFor now, keeping old schema unchanged.")
                    break
                
                elif choice == '2':
                    confirm = input("\n⚠ Are you SURE? This may break existing presets! (type 'yes' to confirm): ")
                    if confirm.lower() == 'yes':
                        self.save_new_schema()
                        print("\n⚠ Schema updated WITHOUT migration.")
                        print("Presets may not work correctly!")
                        break
                    else:
                        print("Cancelled. Choose another option.")
                        continue
                
                elif choice == '3':
                    print("\nCancelled. Keeping old schema.")
                    break
                
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
        
        else:
            # Only cosmetic changes - safe to update automatically
            print("\n✓ All changes are cosmetic (display labels, expressions)")
            print("Safe to update schema without migration.")
            
            confirm = input("\nUpdate schema? (y/n): ").lower()
            if confirm == 'y':
                self.save_new_schema()
                print("\n✓ Schema updated successfully!")
            else:
                print("\nCancelled. Keeping old schema.")

def main():
    """Main entry point for schema comparison"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Extract and compare element schemas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full workflow (extract, compare, prompt for migration)
  python -m core.preset_administration.schema_comparator
  
  # Use custom schema file location
  python -m core.preset_administration.schema_comparator --schema-file /path/to/schemas.json
        """
    )
    parser.add_argument('--schema-file', 
                       default='element_schemas.json',
                       help='Path to schema file (default: element_schemas.json in current dir)')
    
    args = parser.parse_args()
    
    comparator = SchemaComparator(schema_file=args.schema_file)
    comparator.run_workflow()

if __name__ == '__main__':
    main()