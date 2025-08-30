import os
from typing import Optional

class Config:
    """Configuration class for MCP Agent Tracker"""
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    DEBUG = ENVIRONMENT == 'development'
    
    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    DB_PATH = os.getenv('DB_PATH', '/Users/jonathanmorand/Documents/ProjectsFolder/MCP_FOLDER/MCP/MCP/data/agent_tracker.db')
    
    # User configuration
    USER_ID = os.getenv('USER_ID', 'anonymous')
    
    # Container configuration
    CONTAINER_ID = os.getenv('HOSTNAME', 'unknown')
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/agent_tracker.log')  # Changed to relative path for local dev
    
    # Performance configuration
    MAX_EXECUTION_TIME_MS = int(os.getenv('MAX_EXECUTION_TIME_MS', '30000'))  # 30 seconds
    BATCH_LOG_SIZE = int(os.getenv('BATCH_LOG_SIZE', '100'))
    
    # MCP configuration
    MCP_TRANSPORT = os.getenv('MCP_TRANSPORT', 'stdio')  # stdio, http, or tcp
    
    # Automatic monitoring configuration
    ENABLE_BACKGROUND_MONITORING = os.getenv('ENABLE_BACKGROUND_MONITORING', 'true').lower() == 'true'
    MONITORING_INTERVAL_SECONDS = int(os.getenv('MONITORING_INTERVAL_SECONDS', '300'))  # 5 minutes
    ENABLE_AUTOMATIC_METADATA = os.getenv('ENABLE_AUTOMATIC_METADATA', 'true').lower() == 'true'
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the appropriate database URL"""
        if cls.DATABASE_URL:
            return cls.DATABASE_URL
        
        # For local development, ensure data directory exists and use SQLite
        os.makedirs('./data', exist_ok=True)
        return f"sqlite:///{cls.DB_PATH}"
    
    @classmethod
    def is_sqlite(cls) -> bool:
        """Check if using SQLite database"""
        return not cls.DATABASE_URL or 'sqlite' in cls.get_database_url()
    
    @classmethod
    def is_postgresql(cls) -> bool:
        """Check if using PostgreSQL database"""
        return cls.DATABASE_URL and 'postgresql' in cls.get_database_url()
    
    @classmethod
    def is_mysql(cls) -> bool:
        """Check if using MySQL database"""
        return cls.DATABASE_URL and ('mysql' in cls.DATABASE_URL or 'mariadb' in cls.get_database_url())
    
    @classmethod
    def get_database_driver(cls) -> Optional[str]:
        """Get the database driver name"""
        if cls.is_postgresql():
            return 'postgresql'
        elif cls.is_mysql():
            return 'mysql'
        elif cls.is_sqlite():
            return 'sqlite'
        return None
