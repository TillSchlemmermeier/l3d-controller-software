import requests
import re
from bs4 import BeautifulSoup
from db_manager import DatabaseManager
import colorsys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import json

def fetch_webgradients():
    """Scrape gradients from webgradients.com"""
    try:
        # List of titles to exclude
        excluded_titles = {
            'Heavy Rain', 'Cloudy Knoxville', 'Saint Petersburg', 'Everlasting Sky',
            'Coup de Grace', 'Loon Crest', 'Snow Again', 'February Ink', 'Kind Steel',
            'Above Clouds', 'Sharp Glass', 'Clean Mirror', 'Premium Dark', 'Cochiti Lake',
            'Mountain Rock', 'Jungle Day', 'Premium White', 'Cloudy Apple', 'Risky Concrete',
            'Strong Stick', 'Vicious Stance', 'Raccoon Back', 'Confident Cloud', 'Elegance',
            'Above The Sky', 'Chemic Aqua', 'Full Metal', 'Glass Water', 'Slick Carbon',
            'Mole Hall', 'Earl Gray', 'Rich Metal', 'Salt Mountain', 'Perfect White', 'Awesome Pine', 'Blessing', 'Deep Relief', 'Dirty Beauty', 'Frozen Dreams', 'Heaven Peach', 'Marble Wall', 'New York'
        }
        
        url = "https://webgradients.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        gradients = []
        
        # Find gradient elements with the correct class
        gradient_elements = soup.find_all('div', class_='gradient')
        
        for element in gradient_elements:
            try:
                # Extract gradient name from gradient__title span
                title_elem = element.find('span', class_='gradient__title')
                if title_elem:
                    full_title = title_elem.get_text().strip()
                    # Remove newlines and extra whitespace
                    full_title = ' '.join(full_title.split())
                    # Remove the preceding number (e.g., "136 North Miracle" -> "North Miracle")
                    name_parts = full_title.split(' ', 1)
                    if len(name_parts) > 1 and name_parts[0].isdigit():
                        name = name_parts[1]
                    else:
                        name = full_title
                    
                    # Skip if the gradient name is in the excluded list
                    if name in excluded_titles:
                        print(f"Skipping excluded gradient: {name}")
                        continue
                        
                else:
                    name = f"Gradient {len(gradients) + 1}"
                
                # Extract CSS gradient from gradient__background div
                background_div = element.find('div', class_='gradient__background')
                if background_div:
                    style = background_div.get('style', '')
                    if 'background-image:' in style:
                        # Extract the gradient CSS
                        css_gradient = style
                        gradients.append({
                            'name': name,
                            'gradient': css_gradient
                        })
                        
            except Exception as e:
                print(f"Error parsing gradient element: {e}")
                continue
        
        return gradients
        
    except requests.RequestException as e:
        print(f"Error fetching webgradients: {e}")
        return []

def css_to_stops(css_gradient):
    """Convert CSS gradient to your format"""
    # Extract color stops from CSS
    # Match hex colors with optional percentages
    pattern = r'#[0-9A-Fa-f]{6}(?:\s+\d+%)?'
    matches = re.findall(pattern, css_gradient)
    
    if not matches:
        return []
    
    stops = []
    colors = []
    positions = []
    
    # Extract colors and positions separately
    for match in matches:
        parts = match.split()
        color = parts[0].upper()
        colors.append(color)
        
        if len(parts) > 1:
            # Has percentage
            pos = int(parts[1].replace('%', ''))
            positions.append(pos)
        else:
            positions.append(None)
    
    # If no positions specified, distribute evenly
    if all(pos is None for pos in positions):
        for i, color in enumerate(colors):
            position = int((i / (len(colors) - 1)) * 100) if len(colors) > 1 else 0
            stops.append([position, color]) 
    else:
        # Use specified positions
        for i, (color, pos) in enumerate(zip(colors, positions)):
            if pos is None:
                # Calculate position for unspecified ones
                pos = int((i / (len(colors) - 1)) * 100)
            stops.append([pos, color]) 
    
    return stops

def create_sample_gradients():
    """Create sample gradients if web scraping fails"""
    return [
        {'name': 'Fire Sunset', 'gradient': 'linear-gradient(45deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%)'},
        {'name': 'Ocean Blue', 'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'},
        {'name': 'Purple Rain', 'gradient': 'linear-gradient(90deg, #8360c3 0%, #2ebf91 100%)'},
        {'name': 'Sunset Orange', 'gradient': 'linear-gradient(120deg, #fa709a 0%, #fee140 100%)'},
        {'name': 'Green Paradise', 'gradient': 'linear-gradient(to right, #0ba360 0%, #3cba92 100%)'},
        {'name': 'Royal Blue', 'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'},
        {'name': 'Pink Dream', 'gradient': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'},
        {'name': 'Golden Hour', 'gradient': 'linear-gradient(120deg, #f6d365 0%, #fda085 100%)'},
        {'name': 'Deep Sea', 'gradient': 'linear-gradient(90deg, #0052d4 0%, #4364f7 50%, #6fb1fc 100%)'},
        {'name': 'Forest Green', 'gradient': 'linear-gradient(to right, #134e5e 0%, #71b280 100%)'},
    ]

def hsv_to_hex(h, s, v):
    """Convert HSV to hex color"""
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255),
        int(rgb[1] * 255), 
        int(rgb[2] * 255)
    ).upper()

def create_single_color_gradients():
    """Create single color gradients from the full hue rainbow"""
    single_colors = []
    
    # Generate 30 colors across the full hue spectrum
    num_colors = 30
    
    for i in range(num_colors):
        # Calculate hue (0 to 1)
        hue = i / num_colors
        
        # Use full saturation and value for vibrant colors
        saturation = [0.5, 0.75, 1.0]
        value = 1.0
        
        for sat in saturation:
            # Convert to hex
            hex_color = hsv_to_hex(hue, sat, value)
            
            # Create gradient with same color at start and end (solid color)
            gradient_data = json.dumps([[0, hex_color], [100, hex_color]])
            
            # Generate a descriptive name based on hue and saturation
            hue_degrees = int(hue * 360)
            color_name = get_color_name(hue_degrees)
            # Determine subtype based on saturation level
            if sat == 1.0:
                sat_name = "Vibrant"
            elif sat == 0.75:
                sat_name = "Medium"
            else:  # sat == 0.5
                sat_name = "Soft"
            
            single_colors.append({
                'name': f"{color_name} ({hue_degrees}°) - {sat_name}",
                'data': gradient_data,
                'subtype': sat_name
            })
    
    return single_colors

def get_color_name(hue_degrees):
    """Get a descriptive color name based on hue degrees"""
    if hue_degrees < 15 or hue_degrees >= 345:
        return "Red"
    elif hue_degrees < 45:
        return "Orange"
    elif hue_degrees < 75:
        return "Yellow"
    elif hue_degrees < 105:
        return "Yellow-Green"
    elif hue_degrees < 135:
        return "Green"
    elif hue_degrees < 165:
        return "Blue-Green"
    elif hue_degrees < 195:
        return "Cyan"
    elif hue_degrees < 225:
        return "Blue"
    elif hue_degrees < 255:
        return "Blue-Violet"
    elif hue_degrees < 285:
        return "Violet"
    elif hue_degrees < 315:
        return "Magenta"
    else:
        return "Red-Violet"

def get_distinguishable_colors():
    """Get 12 most distinguishable colors"""
    return {
        'Red': '#FF0000',
        'Orange': '#FF8000', 
        'Yellow': '#FFFF00',
        'Yellow-Green': '#80FF00',
        'Green': '#00FF00',
        'Blue-Green': '#00FF80',
        'Cyan': '#00FFFF',
        'Blue': '#0080FF',
        'Navy': '#0000FF',
        'Purple': '#8000FF',
        'Magenta': '#FF00FF',
        'Pink': '#FF0080'
    }

def hex_to_rgb(hex_color):
    """Convert hex to RGB tuple (0-255)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_extended_colors():
    """Get extended color set with full and reduced saturation"""
    base_colors = get_distinguishable_colors()
    extended = {}
    
    for name, hex_color in base_colors.items():
        # Add full saturation version
        extended[f"{name} (Vibrant)"] = hex_color
        
        # Add 0.75 saturation version
        rgb = hex_to_rgb(hex_color)
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        h, s, v = hsv
        s_new = 0.75
        rgb_new = colorsys.hsv_to_rgb(h, s_new, v)
        hex_new = "#{:02x}{:02x}{:02x}".format(
            int(rgb_new[0]*255), 
            int(rgb_new[1]*255), 
            int(rgb_new[2]*255)
        ).upper()
        extended[f"{name} (Soft)"] = hex_new
    
    return extended

def create_two_color_gradients():
    """Create all possible two-color combinations from extended color set"""
    colors = get_extended_colors()
    color_names = list(colors.keys())
    color_values = list(colors.values())
    
    two_color_gradients = []
    
    # Create all combinations (excluding same color combinations)
    for i in range(len(color_names)):
        for j in range(i + 1, len(color_names)):
            color1_name = color_names[i]
            color2_name = color_names[j]
            color1_hex = color_values[i]
            color2_hex = color_values[j]
            
            # Determine subtype based on saturation levels
            color1_sat = "Vibrant" if "Vibrant" in color1_name else "Soft"
            color2_sat = "Vibrant" if "Vibrant" in color2_name else "Soft"
            
            if color1_sat == color2_sat:
                subtype = color1_sat
            else:
                subtype = "Mixed"
            
            # Create gradient from color1 to color2
            gradient_data = json.dumps([[0, color1_hex], [100, color2_hex]])
            name = f"{color1_name} to {color2_name}"
            
            two_color_gradients.append({
                'name': name,
                'data': gradient_data,
                'subtype': subtype 
            })
    
    return two_color_gradients


def matplotlib_to_gradient_stops(cmap_name, num_stops=6):
    """Convert matplotlib colormap to gradient stops format"""
    try:
        cmap = plt.get_cmap(cmap_name)
        stops = []
        
        for i in range(num_stops):
            # Position from 0 to 100
            position = int((i / (num_stops - 1)) * 100)
            
            # Get normalized position (0 to 1) for colormap
            norm_pos = i / (num_stops - 1)
            
            # Get RGBA color from colormap
            rgba = cmap(norm_pos)
            
            # Convert to hex (ignore alpha channel)
            hex_color = mcolors.rgb2hex(rgba[:3]).upper()
            
            stops.append([position, hex_color])
        
        return stops
    except Exception as e:
        print(f"Error processing colormap {cmap_name}: {e}")
        return []

def get_matplotlib_colormaps():
    """Get matplotlib colormaps organized by subtype"""
    return {
        'Sequential': [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis',
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
        ],
        'Sequential 2': [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
            'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
            'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'
        ],
        'Diverging': [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'
        ],
        'Cyclic': [
            'twilight', 'twilight_shifted', 'hsv'
        ],
        'Miscellaneous': [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
            'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
            'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
            'turbo', 'nipy_spectral', 'gist_ncar'
        ]
    }

def create_matplotlib_gradients():
    """Create matplotlib colormap gradients"""
    matplotlib_gradients = []
    colormaps = get_matplotlib_colormaps()
    
    for subtype, cmap_names in colormaps.items():
        for cmap_name in cmap_names:
            try:
                # Determine optimal number of stops
                if subtype in ['Sequential', 'Sequential 2']:
                    num_stops = 4
                elif subtype == 'Diverging':
                    num_stops = 5
                elif subtype == 'Cyclic':
                    num_stops = 8
                else:  # Miscellaneous
                    num_stops = 6
                
                # Extract gradient stops
                stops = matplotlib_to_gradient_stops(cmap_name, num_stops)
                
                if len(stops) >= 2:
                    gradient_data = json.dumps(stops)

                    matplotlib_gradients.append({
                        'name': cmap_name.title(),
                        'subtype': subtype,
                        'data': gradient_data
                    })
                    
            except Exception as e:
                print(f"Error processing matplotlib colormap {cmap_name}: {e}")
                continue
    
    return matplotlib_gradients

def populate_webgradients_database():
    """Populate database with all gradient types"""
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    successful_imports = 0
    failed_imports = 0
    
    # 1. Process webgradients
    print("Fetching gradients from webgradients.com...")
    webgradients = fetch_webgradients()
    
    if not webgradients:
        print("Web scraping failed, using sample gradients...")
        webgradients = create_sample_gradients()
    
    for gradient in webgradients:
        try:
            name = gradient.get('name', 'Unnamed')
            css_gradient = gradient.get('gradient', '')
            
            if not css_gradient:
                failed_imports += 1
                continue
            
            stops = css_to_stops(css_gradient)
            if len(stops) < 2:
                failed_imports += 1
                continue
            
            gradient_data = json.dumps(stops)
            success, message = db_manager.save_gradient(
                gradient_type='webgradients',
                data=gradient_data
            )
            
            if success:
                print(f"✓ Saved webgradient: {name}")
                successful_imports += 1
            else:
                print(f"✗ Failed to save {name}: {message}")
                failed_imports += 1
                
        except Exception as e:
            print(f"✗ Error processing {gradient.get('name', 'Unknown')}: {e}")
            failed_imports += 1
    
    # 2. Create matplotlib gradients
    print("\nGenerating matplotlib gradients...")
    matplotlib_gradients = create_matplotlib_gradients()
    
    for gradient in matplotlib_gradients:
        try:
            success, message = db_manager.save_gradient(
                gradient_type='matplotlib',
                data=gradient['data'],
                subtype=gradient['subtype']
            )
            
            if success:
                print(f"✓ Saved matplotlib: {gradient['name']} ({gradient['subtype']})")
                successful_imports += 1
            else:
                print(f"✗ Failed to save {gradient['name']}: {message}")
                failed_imports += 1
                
        except Exception as e:
            print(f"✗ Error processing matplotlib {gradient['name']}: {e}")
            failed_imports += 1
    
    # 3. Create single color gradients
    print("\nGenerating single color gradients...")
    single_colors = create_single_color_gradients()
    
    for color_gradient in single_colors:
        try:
            success, message = db_manager.save_gradient(
                gradient_type='single_colors',
                data=color_gradient['data'],
                subtype=color_gradient['subtype']
            )
            
            if success:
                print(f"✓ Saved single color: {color_gradient['name']}")
                successful_imports += 1
            else:
                failed_imports += 1
                
        except Exception as e:
            failed_imports += 1
    
    # 4. Create two-color gradients
    print("\nGenerating two-color gradients...")
    two_color_gradients = create_two_color_gradients()
    
    for color_gradient in two_color_gradients:
        try:
            success, message = db_manager.save_gradient(
                gradient_type='two_colors',
                data=color_gradient['data'],
                subtype=color_gradient['subtype']
            )
            
            if success:
                print(f"✓ Saved two-color: {color_gradient['name']}")
                successful_imports += 1
            else:
                failed_imports += 1
                
        except Exception as e:
            failed_imports += 1
    
    total_processed = len(webgradients) + len(matplotlib_gradients) + len(single_colors) + len(two_color_gradients)
    
    print(f"\nImport complete:")
    print(f"  Webgradients: {len(webgradients)}")
    print(f"  Matplotlib gradients: {len(matplotlib_gradients)}")
    print(f"  Single colors: {len(single_colors)}")
    print(f"  Two-color gradients: {len(two_color_gradients)}")
    print(f"  Successful imports: {successful_imports}")
    print(f"  Failed imports: {failed_imports}")
    print(f"  Total processed: {total_processed}")

def main():
    """Main function to run the import"""
    populate_webgradients_database()

if __name__ == "__main__":
    main()