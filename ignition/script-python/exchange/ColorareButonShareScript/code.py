def runAction(self, event):
# Step 1: Get parent container and loop through its children
	parent = self.getParent()
	for child in parent.getChildren():
		# Skip the clicked component itself
		if child != self:
			child.custom.toggled = False
			child.props.style = {
				"classes": "Shadow",
				"overflow": "auto",
				"borderBottomLeftRadius": 15,
				"borderBottomRightRadius": 15,
				"borderTopLeftRadius": 15,
				"borderTopRightRadius": 15,
				"boxShadow": "none",
				"backgroundColor": "transparent",
				"cursor": "pointer"
			}
			# 🔄 Reset label text color inside other containers
			for grandchild in child.getChildren():
				if grandchild.meta.name == "Label":
					grandchild.props.style = {
						"color": "#937D7D"  # default color
					}

	# Step 2: Toggle clicked component (self)
	current = self.custom.get("toggled", False)
	self.custom.toggled = not current

	if self.custom.toggled:
		self.props.style = {
			"classes": "Shadow",
			"overflow": "auto",
			"borderBottomLeftRadius": 15,
			"borderBottomRightRadius": 15,
			"borderTopLeftRadius": 15,
			"borderTopRightRadius": 15,
			"backgroundColor": "rgba(37, 56, 79)",
			"cursor": "pointer"
		}
		# 🔷 Change label color to highlighted
		for child in self.getChildren():
			if child.meta.name == "Label":
				child.props.style = {
					"color": "#FFFFFF"  # white or any highlight color
				}
	else:
		self.props.style = {
			"classes": "Shadow",
			"overflow": "auto",
			"borderBottomLeftRadius": 15,
			"borderBottomRightRadius": 15,
			"borderTopLeftRadius": 15,
			"borderTopRightRadius": 15,
			"boxShadow": "none",
			"backgroundColor": "transparent",
			"cursor": "pointer"
		}
		# 🔄 Reset label text color
		for child in self.getChildren():
			if child.meta.name == "Label":
				child.props.style = {
					"color": "#937D7D"  # default color
				}