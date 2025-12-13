"""
Tag reading helper functions for Ignition SCADA systems.
Jython 2.7 compatible - no f-strings, no typing, no asyncio.
"""
import random

def read_tag_safe(tag_path, default_value=None):
    """
    Safely reads a tag and returns default value if tag has bad quality.
    
    Args:
        tag_path (str): The path to the tag to read (e.g., "[default]MyTag")
        default_value: The value to return if tag quality is bad or read fails.
                       Defaults to None.
    
    Returns:
        The tag value if quality is good, otherwise returns default_value.
    
    Example:
        value = read_tag_safe("[default]Temperature", 0.0)
        # Returns tag value if good quality, otherwise returns 0.0
    """
    try:
        # Read the tag
        tag_data = system.tag.read(tag_path)
        
        # Check if read was successful and tag exists
        if tag_data is None:
            return default_value
        
        # Check tag quality - "Good" indicates valid data
        # Bad quality can be "Bad", "Uncertain", "Error", etc.
        if hasattr(tag_data, 'quality') and tag_data.quality == "Good":
            return tag_data.value
        else:
            return default_value
            
    except Exception, e:
        # Log error if logging is available, but don't fail
        # Return default value on any exception
        try:
            system.util.getLogger("TagHelpers").warn(
                "Failed to read tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass  # Ignore logging errors
        
        return default_value


def read_tags_safe(tag_paths, default_value=None):
    """
    Safely reads multiple tags and returns default value for any tags with bad quality.
    
    Args:
        tag_paths (list): List of tag paths to read
        default_value: The value to return for tags with bad quality or that fail to read.
                       Defaults to None.
    
    Returns:
        List of tag values. Values with bad quality are replaced with default_value.
    
    Example:
        values = read_tags_safe(["[default]Temp1", "[default]Temp2"], 0.0)
    """
    if not tag_paths:
        return []
    
    try:
        # Read all tags at once
        tag_data_list = system.tag.readAll(tag_paths)
        
        results = []
        for i, tag_data in enumerate(tag_data_list):
            if tag_data is None:
                results.append(default_value)
            elif hasattr(tag_data, 'quality') and tag_data.quality == "Good":
                results.append(tag_data.value)
            else:
                results.append(default_value)
        
        return results
        
    except Exception, e:
        # On error, return list of default values
        try:
            system.util.getLogger("TagHelpers").warn(
                "Failed to read tags: {}".format(str(e))
            )
        except:
            pass
        
        return [default_value] * len(tag_paths)


def create_tag(tag_path, tag_type="Memory", data_type="Float", value=None):
    """
    Creates a new tag in Ignition.
    
    Args:
        tag_path (str): The full path to the tag (e.g., "[default]MyTag")
        tag_type (str): Type of tag - "Memory", "Expression", "Query", etc. Defaults to "Memory"
        data_type (str): Data type - "Float", "Int", "String", "Boolean", etc. Defaults to "Float"
        value: Initial value for the tag. Defaults to None (0.0 for numeric types)
    
    Returns:
        bool: True if tag was created successfully, False otherwise
    
    Example:
        create_tag("[default]RandomValue", "Memory", "Float", 0.0)
    """
    try:
        # Parse tag path to get provider and tag name
        if tag_path.startswith("["):
            end_bracket = tag_path.index("]")
            provider = tag_path[1:end_bracket]
            tag_name = tag_path[end_bracket + 1:]
        else:
            provider = "default"
            tag_name = tag_path
        
        # Build tag configuration
        tag_config = {
            "tagType": tag_type,
            "name": tag_name,
            "valueType": data_type
        }
        
        # Set initial value if provided
        if value is not None:
            tag_config["value"] = value
        
        # Configure the tag
        result = system.tag.configureBaseTags([tag_config], provider)
        
        # Check if configuration was successful
        if result and len(result) > 0:
            return True
        else:
            return False
            
    except Exception, e:
        try:
            system.util.getLogger("TagHelpers").error(
                "Failed to create tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return False


def generate_random_value(tag_path, min_value=0.0, max_value=100.0, data_type="Float"):
    """
    Generates a random value and writes it to the specified tag.
    Creates the tag if it doesn't exist.
    
    Args:
        tag_path (str): The path to the tag (e.g., "[default]RandomValue")
        min_value: Minimum value for random generation. Defaults to 0.0
        max_value: Maximum value for random generation. Defaults to 100.0
        data_type (str): Data type of the tag - "Float", "Int", "Boolean", etc. Defaults to "Float"
    
    Returns:
        The generated random value, or None if failed
    
    Example:
        # Generate random float between 0 and 100
        value = generate_random_value("[default]RandomValue", 0.0, 100.0, "Float")
        
        # Generate random integer between 1 and 100
        value = generate_random_value("[default]RandomInt", 1, 100, "Int")
        
        # Generate random boolean
        value = generate_random_value("[default]RandomBool", 0, 1, "Boolean")
    """
    try:
        # Generate random value based on data type
        if data_type == "Int":
            random_value = random.randint(int(min_value), int(max_value))
        elif data_type == "Boolean":
            random_value = bool(random.randint(0, 1))
        elif data_type == "String":
            # For strings, generate random alphanumeric string
            length = int(min_value) if min_value > 0 else 10
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            random_value = ''.join(random.choice(chars) for _ in range(length))
        else:
            # Default to Float
            random_value = random.uniform(float(min_value), float(max_value))
        
        # Write the random value to the tag
        write_result = system.tag.write(tag_path, random_value)
        
        if write_result:
            return random_value
        else:
            # Tag might not exist, try to create it first
            if create_tag(tag_path, "Memory", data_type, random_value):
                return random_value
            return None
            
    except Exception, e:
        try:
            system.util.getLogger("TagHelpers").error(
                "Failed to generate random value for tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return None


def create_and_start_random_tag(tag_path, min_value=0.0, max_value=100.0, 
                                data_type="Float", update_interval_sec=1.0):
    """
    Creates a tag and sets up an expression to continuously generate random values.
    The tag will update automatically at the specified interval.
    
    Args:
        tag_path (str): The path to the tag (e.g., "[default]RandomValue")
        min_value: Minimum value for random generation. Defaults to 0.0
        max_value: Maximum value for random generation. Defaults to 100.0
        data_type (str): Data type - "Float", "Int", etc. Defaults to "Float"
        update_interval_sec (float): Update interval in seconds. Defaults to 1.0
    
    Returns:
        bool: True if tag was created and configured successfully, False otherwise
    
    Example:
        # Create tag that generates random floats between 0-100 every second
        create_and_start_random_tag("[default]RandomValue", 0.0, 100.0, "Float", 1.0)
    """
    try:
        # Parse tag path
        if tag_path.startswith("["):
            end_bracket = tag_path.index("]")
            provider = tag_path[1:end_bracket]
            tag_name = tag_path[end_bracket + 1:]
        else:
            provider = "default"
            tag_name = tag_path
        
        # Build expression based on data type
        if data_type == "Int":
            expr = "random.randint({}, {})".format(int(min_value), int(max_value))
        elif data_type == "Boolean":
            expr = "random.randint(0, 1) == 1"
        else:
            # Float
            expr = "random.uniform({}, {})".format(float(min_value), float(max_value))
        
        # Build tag configuration for Expression tag
        tag_config = {
            "tagType": "Expression",
            "name": tag_name,
            "valueType": data_type,
            "expression": expr,
            "scanRateMs": int(update_interval_sec * 1000)
        }
        
        # Configure the tag
        result = system.tag.configureBaseTags([tag_config], provider)
        
        # Make sure random module is imported in expression context
        # This needs to be done separately in Ignition's expression context
        
        if result and len(result) > 0:
            # Initialize with first random value
            if data_type == "Int":
                initial_value = random.randint(int(min_value), int(max_value))
            elif data_type == "Boolean":
                initial_value = bool(random.randint(0, 1))
            else:
                initial_value = random.uniform(float(min_value), float(max_value))
            
            system.tag.write(tag_path, initial_value)
            return True
        else:
            return False
            
    except Exception, e:
        try:
            system.util.getLogger("TagHelpers").error(
                "Failed to create random tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return False
