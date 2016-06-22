from __future__ import with_statement, absolute_import

import os.path

from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .errors import ConfigurationFileInitialized,\
    ConfigurationFileNotFound


class ConfigBase(object):
    def __init__(self, config_file_path):
        self.options = load(open(config_file_path))


class Config(ConfigBase):
    def __init__(self, config_file_path, generate_if_not_found=True):
        if not os.path.isfile(config_file_path):
            if generate_if_not_found:
                self.reset_configfile(config_file_path)
            if os.path.isfile(config_file_path):
                raise ConfigurationFileInitialized("""No configuration file found.
A new file has been initialized at: %s
Please review the configuration and retry...""" % config_file_path)
            else:
                raise ConfigurationFileNotFound("cannot load config file %s" % config_file_path)

        super(Config, self).__init__(config_file_path)

    def reset_configfile(self, file_path):
        with open(file_path, 'w') as f:
            f.write(CONFIG_TEMPLATE)

CONFIG_TEMPLATE = """
# a socket connection will be selected if a 'socket' is specified
# also 'localhost' is a special 'hostname' for MySQL that overrides the 'port' option
# and forces it to use a local socket connection
# if tcp is chosen, you can use compression

mysql:
 hostname: localhost
 port: 3306
 socket: /tmp/mysql.sock
 username: mysql2psql
 password: 
 database: mysql2psql_test
 compress: false
destination:
 # if file is given, output goes to file, else postgres
 file: 
 postgres:
  hostname: localhost
  port: 5432
  username: mysql2psql
  password: 
  database: mysql2psql_test

# if tables is given, only the listed tables will be converted.  leave empty to convert all tables.
#only_tables:
#- table1
#- table2
# if exclude_tables is given, exclude the listed tables from the conversion.
#exclude_tables:
#- table3
#- table4

do_data: false
do_pre: false
do_post: false
truncate: false

# if timezone is true, forces to append/convert to UTC tzinfo mysql data
timezone: false

# if index_prefix is given, indexes will be created whith a name prefixed with index_prefix
index_prefix:

"""
