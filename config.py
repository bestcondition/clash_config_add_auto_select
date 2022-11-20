class MyConfig:
    HOST: str = '0.0.0.0'
    PORT: int = 42843
    PROXY_URL: str = 'http://localhost:7890'
    PING_URL: str = 'http://www.gstatic.com/generate_204'


def get_config() -> MyConfig:
    return MyConfig()


config = get_config()
