

class Plugin:

    """
    Main class for installing custom plugin 
    
    Github Repository Structure should look like this

    repoName/
        ext/ - Here the cogs stored
            cogs01.py 
        main.py - A main handler for your cogs. 
        config.json - Handle every settings
    
    """

    def __init__(self, repository):
        self.repo = repository
