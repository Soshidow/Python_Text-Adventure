# Python_Text-Adventure
 Text-based 'Choose Your Own Adventure'

	Version 2:
		+ Rewritten from the ground up to accommodate scalability
		+ Functions and Classes code kept in separate files for readability
		+ Abstraction of code by containing game object logic within classes
		+ Inheritance with object subclasses for more specific use objects.
		+ The game now reads from a map (a text file) to create its world
			+ newlines are Y coordinates
			+ tabs are X coordinates
			+ the words used must match the 'name' argument you pass to an object (otherwise it will be ignored)