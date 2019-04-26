import os
import yaml
from common_utils import MetaSingleton

app_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.abspath(os.path.dirname(app_path))
configs_path = os.path.join(base_path,'configs/')



app_env = os.getenv('APP_ENV') if os.getenv('APP_ENV') else 'default'

class FileConfig(metaclass=MetaSingleton):
    def __init__(self,cfg_file='default_configs.yaml'):
        self._yaml_cfg = FileConfig.__get_config_file(cfg_file)
        self.server_cfg = self._yaml_cfg.get('server',None)
        self.mysql_cfg = self._yaml_cfg.get('mysql',None)
        self.redis_cfg = self._yaml_cfg.get("redis",None)

    @staticmethod
    def __get_config_file(cfg_file):
        cfg_path = os.path.join(configs_path,cfg_file)
        if os.path.exists(cfg_path) and os.path.isfile(cfg_path):
            with open(cfg_path,encoding='utf-8') as f:
                return yaml.load(f.read())
    @staticmethod
    def get_config():
        if 'development' == app_env:
            return FileConfig('development_configs.yaml')
        elif 'production' == app_env:
            return FileConfig('production_configs.yaml')
        else:
            return FileConfig('default_configs.yaml')


class ServerConfig(metaclass=MetaSingleton):
    def __init__(self):
        for k,v in FileConfig.get_config().server_cfg.items():
            object.__setattr__(self,k,v)



class MysqlConfig(metaclass=MetaSingleton):
    def __init__(self):
        for k,v in FileConfig.get_config().mysql_cfg.items():
            object.__setattr__(self,k,v)
    def get_uri(self):
        return self.uri



class RedisConfig(metaclass=MetaSingleton):
    def __init__(self):
        for k,v in FileConfig.get_config().redis_cfg.items():
            object.__setattr__(self,k,v)