class GlobalState:
    _instance = None
    
    failed_daily_tasks = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalState, cls).__new__(cls)
        return cls._instance