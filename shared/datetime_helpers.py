"""
Datetime tag helper functions for Ignition SCADA systems.
Jython 2.7 compatible - no f-strings, no typing, no asyncio.
"""
from java.util import Date
from java.text import SimpleDateFormat

def create_tag(tag_path, tag_type="Memory", data_type="String", value=None):
    """
    Helper function to create a tag in Ignition.
    
    Args:
        tag_path (str): The full path to the tag (e.g., "[default]MyTag")
        tag_type (str): Type of tag - "Memory", "Expression", etc. Defaults to "Memory"
        data_type (str): Data type - "String", "Float", "Int", etc. Defaults to "String"
        value: Initial value for the tag. Defaults to None
    
    Returns:
        bool: True if tag was created successfully, False otherwise
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
            system.util.getLogger("DateTimeHelpers").error(
                "Failed to create tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return False


def create_datetime_tag(tag_path):
    """
    Creates a tag and writes the current datetime to it.
    
    Args:
        tag_path (str): The path to the tag (e.g., "[default]CurrentDateTime")
    
    Returns:
        str: The formatted datetime string that was written, or None if failed
    
    Example:
        datetime_str = create_datetime_tag("[default]CurrentDateTime")
    """
    try:
        # Get current datetime
        now = Date()
        date_format = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        datetime_str = date_format.format(now)
        
        # Try to write to tag
        write_result = system.tag.write(tag_path, datetime_str)
        
        if write_result:
            return datetime_str
        else:
            # Tag might not exist, try to create it first
            if create_tag(tag_path, "Memory", "String", datetime_str):
                return datetime_str
            return None
            
    except Exception, e:
        try:
            system.util.getLogger("DateTimeHelpers").error(
                "Failed to create datetime tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return None


def create_tag_with_current_datetime(tag_path, tag_type="Memory", date_format_pattern="yyyy-MM-dd HH:mm:ss"):
    """
    Creates a new tag and writes the current datetime to it.
    
    Args:
        tag_path (str): The full path to the tag (e.g., "[default]MyDateTimeTag")
        tag_type (str): Type of tag - "Memory", "Expression", etc. Defaults to "Memory"
        date_format_pattern (str): Date format pattern (Java SimpleDateFormat). 
                                   Defaults to "yyyy-MM-dd HH:mm:ss"
    
    Returns:
        str: The formatted datetime string, or None if failed
    
    Example:
        # Create tag with default format (yyyy-MM-dd HH:mm:ss)
        create_tag_with_current_datetime("[default]CurrentTime")
        
        # Create tag with custom format
        create_tag_with_current_datetime("[default]DateOnly", "Memory", "yyyy-MM-dd")
        create_tag_with_current_datetime("[default]TimeOnly", "Memory", "HH:mm:ss")
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
        
        # Get current datetime and format it
        now = Date()
        date_format = SimpleDateFormat(date_format_pattern)
        datetime_str = date_format.format(now)
        
        # Create tag configuration
        tag_config = {
            "tagType": tag_type,
            "name": tag_name,
            "valueType": "String",
            "value": datetime_str
        }
        
        # Configure the tag
        result = system.tag.configureBaseTags([tag_config], provider)
        
        if result and len(result) > 0:
            return datetime_str
        else:
            return None
            
    except Exception, e:
        try:
            system.util.getLogger("DateTimeHelpers").error(
                "Failed to create datetime tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return None


def update_tag_with_datetime(tag_path, date_format_pattern="yyyy-MM-dd HH:mm:ss"):
    """
    Updates an existing tag with the current datetime.
    
    Args:
        tag_path (str): The path to the tag (e.g., "[default]CurrentDateTime")
        date_format_pattern (str): Date format pattern (Java SimpleDateFormat).
                                   Defaults to "yyyy-MM-dd HH:mm:ss"
    
    Returns:
        str: The formatted datetime string, or None if failed
    
    Example:
        # Update with default format
        datetime_str = update_tag_with_datetime("[default]CurrentDateTime")
        
        # Update with custom format
        datetime_str = update_tag_with_datetime("[default]MyTag", "dd/MM/yyyy HH:mm")
    """
    try:
        # Get current datetime and format it
        now = Date()
        date_format = SimpleDateFormat(date_format_pattern)
        datetime_str = date_format.format(now)
        
        # Write to tag
        write_result = system.tag.write(tag_path, datetime_str)
        
        if write_result:
            return datetime_str
        else:
            return None
            
    except Exception, e:
        try:
            system.util.getLogger("DateTimeHelpers").error(
                "Failed to update datetime tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return None


def create_auto_update_datetime_tag(tag_path, update_interval_sec=1.0, 
                                    date_format_pattern="yyyy-MM-dd HH:mm:ss"):
    """
    Creates a tag with an expression that automatically updates with current datetime.
    The tag will update automatically at the specified interval.
    
    Args:
        tag_path (str): The path to the tag (e.g., "[default]AutoDateTime")
        update_interval_sec (float): Update interval in seconds. Defaults to 1.0
        date_format_pattern (str): Date format pattern (Java SimpleDateFormat).
                                   Defaults to "yyyy-MM-dd HH:mm:ss"
    
    Returns:
        bool: True if tag was created successfully, False otherwise
    
    Example:
        # Create tag that updates every second with current datetime
        create_auto_update_datetime_tag("[default]AutoDateTime", 1.0)
        
        # Create tag that updates every 5 seconds
        create_auto_update_datetime_tag("[default]AutoDateTime", 5.0)
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
        
        # Build expression for current datetime
        # Note: In Ignition expressions, we can use Java Date and SimpleDateFormat
        expr = 'SimpleDateFormat("{}").format(Date())'.format(date_format_pattern)
        
        # Build tag configuration for Expression tag
        tag_config = {
            "tagType": "Expression",
            "name": tag_name,
            "valueType": "String",
            "expression": expr,
            "scanRateMs": int(update_interval_sec * 1000)
        }
        
        # Configure the tag
        result = system.tag.configureBaseTags([tag_config], provider)
        
        if result and len(result) > 0:
            # Initialize with current datetime
            now = Date()
            date_format = SimpleDateFormat(date_format_pattern)
            initial_value = date_format.format(now)
            system.tag.write(tag_path, initial_value)
            return True
        else:
            return False
            
    except Exception, e:
        try:
            system.util.getLogger("DateTimeHelpers").error(
                "Failed to create auto-update datetime tag '{}': {}".format(tag_path, str(e))
            )
        except:
            pass
        return False
