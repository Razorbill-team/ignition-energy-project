def onStartup():
	"""
	Creates 10 random tags (tag1-tag10) at startup if they don't already exist.
	Tags will generate random float values between 0 and 100.
	"""
	import random
	
	# Tag provider - adjust if needed
	tag_provider = "default"
	
	# Base tag path
	base_path = "[{}]".format(tag_provider)
	
	# Create tags tag1 through tag10
	for i in range(1, 11):
		tag_name = "tag{}".format(i)
		tag_path = base_path + tag_name
		
		try:
			# Check if tag already exists by trying to read it
			tag_data = system.tag.read(tag_path)
			
			# If tag exists (even with bad quality), skip creation
			if tag_data is not None:
				system.util.getLogger("Startup").info(
					"Tag '{}' already exists, skipping creation".format(tag_path)
				)
				continue
		except Exception, e:
			# Tag doesn't exist or read failed - proceed with creation
			# This is expected when tag doesn't exist, so we don't log it
			pass
		
		try:
			# Create tag as Expression type that generates random values
			# Random float between 0 and 100 using Java Math.random()
			# Math.random() returns value between 0.0 and 1.0, multiply by 100
			expr = "Math.random() * 100.0"
			
			tag_config = {
				"tagType": "Expression",
				"name": tag_name,
				"valueType": "Float",
				"expression": expr,
				"scanRateMs": 1000  # Update every second
			}
			
			# Configure the tag
			result = system.tag.configureBaseTags([tag_config], tag_provider)
			
			if result and len(result) > 0:
				# Initialize with first random value
				initial_value = random.uniform(0.0, 100.0)
				system.tag.write(tag_path, initial_value)
				
				system.util.getLogger("Startup").info(
					"Successfully created tag '{}' with initial value: {}".format(
						tag_path, initial_value
					)
				)
			else:
				system.util.getLogger("Startup").warn(
					"Failed to create tag '{}'".format(tag_path)
				)
				
		except Exception, e:
			system.util.getLogger("Startup").error(
				"Error creating tag '{}': {}".format(tag_path, str(e))
			)
	
	system.util.getLogger("Startup").info("Startup script completed: tag1-tag10 initialization")