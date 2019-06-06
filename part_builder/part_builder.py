#!/usr/bin/env python3
"""
    Builds the docker-compose file using modular
    components specified by the user

    Also builds the NGINX router default.conf
    containing the routing for desired services

    Functions primarily do text appending,
    CLI logic is enclosed in synth.py
"""
import os
from part_builder import PartBuilderException


class PartBuilder():
    """
        Part builder class for use with building the compose file
        and nginx router file
    """
    allowed_frontends = ['static', 'node', 'react', 'reactjs']
    allowed_backends = ['node', 'flask', 'django']
    allowed_databases = ['mongo', 'postgres', 'mysql']
    allowed_caches = ['redis', 'memcache']

    def __init__(self, parts_root=None, nginx_file=None, compose_file=None):
        """
            Init method for class, sets important path information
        """
        # do some checking on the config info passed
        self.str_check(
            parts_root, "root to parts directory must be of type string in PartBuilder init function")
        self.str_check(
            nginx_file, "default.conf file for NGINX router must be of type string in PartBuilder init function")
        self.str_check(
            compose_file, "compose file must be of type string in PartBuilder init function")
        if not self.isfile_check:
            raise PartBuilderException(
                nginx_file, "{} is not a file or does not exist".format(nginx_file))
        if not self.isfile_check:
            raise PartBuilderException(
                compose_file, "{} is not a file or does not exist".format(
                    compose_file)
            )

        # if all is good we got here without raising an exception, set instance to init info
        self.parts_root = parts_root
        self.nginx_file = nginx_file
        self.compose_file = compose_file
        self.allowed_master = []
        self.allowed_master.extend(self.allowed_frontends)
        self.allowed_master.extend(self.allowed_backends)
        self.allowed_master.extend(self.allowed_databases)
        self.allowed_master.extend(self.allowed_caches)

    @staticmethod
    def str_check(param=None, err_msg="Path Error"):
        """
            Checks that variables passed to PartBuilder functions
            are not None and exist

            Based on:
                param: variable to check
                err_msg: error message to output
        """
        if param is None:
            raise PartBuilderException(err_msg)
        elif type(param) != str:
            raise PartBuilderException(err_msg)

    @staticmethod
    def isfile_check(path=None):
        """
            Checks if a file exists at a given path

            Based on:
                path: string containing file path to check
        """
        if path is None:
            return False
        return os.path.isfile(path)

    def add_part(self, part=None):
        """
            adds a part to compose and nginx files based on a string passed

            Based on:
                part: string representing part to add,
                    e.g: static
        """
        self.str_check(
            part, "PartBuilder cannot add part of type {}".format(type(part)))
        part = part.lower()
        # append neccessary content for the part to the compose and nginx config files
        if part in self.allowed_master:
            self.compose_add(self.parts_root +
                             '/compose/{}.part'.format(part), self.compose_file)
            self.upstream_add(self.parts_root +
                              '/nginx/upstream/{}.part'.format(part), self.nginx_file)
            self.location_add(self.parts_root +
                              '/nginx/location/{}.part'.format(part), self.nginx_file)
        else:
            raise PartBuilderException(
                "part provided to PartBuilder ({}) is not in allowed_master".format(part))

    def compose_add(self, part_path=None, config_path=None):
        """
            Adds a part to the master docker-compose file

            Based on:
                part_path: path to the part to add
                compose_path: path to master compose file to add to
        """
        path_err = "Path to compose service part (part_path) must be of string type"
        config_err = "Path to docker-compose file (config_path) must be of string type"

        self.str_check(part_path, path_err)
        self.str_check(config_path, config_err)
        # all parts should have a compose portion
        if self.isfile_check(part_path) is False:
            raise PartBuilderException(
                "{} is not a file or did not exist.".format(part_path))
        # TODO add the actual append logic
        print('debug: adding compose portion for{} in file {}'.format(
            part_path, config_path))
        # read the part file and config file text
        with open(part_path, 'r') as part_file:
            part_data = part_file.readlines()
        with open(config_path, 'r') as file:
            cur_config = file.readlines()
        # add the part text onto the front of the config
        cur_config.extend(part_data)
        # write the new compose config file
        with open(config_path, 'w') as new_config:
            new_config.writelines(cur_config)

    def upstream_add(self, part_path=None, config_path=None):
        """
            Adds an upstream to the NGINX router default.conf file

            ONLY needed for frontend and backend portions

            Based on:
                part_path: path to the part containing the upstream
                config_path: path to the NGINX router default.conf file
        """
        path_err = "Path to upstream part (part_path) must be of string type"
        config_err = "Path to NGINX router file (config_path) must be of string type"

        self.str_check(part_path, path_err)
        self.str_check(config_path, config_err)
        # skip if it's not present (not an error b/c database and cache are always not present)
        if self.isfile_check(part_path) is False:
            return None
        print('debug: adding upstream portion for {} in file {}'.format(
            part_path, config_path))
        # read the part file and config file text
        with open(part_path, 'r') as part_file:
            part_data = part_file.readlines()
        with open(config_path, 'r') as file:
            cur_config = file.readlines()
        # add the part text onto the front of the config
        part_data.extend(cur_config)
        # write the new NGINX config file
        with open(config_path, 'w') as new_config:
            new_config.writelines(part_data)

    def location_add(self, part_path=None, config_path=None):
        """
            Adds a location block to the server block in the NGINX router
            default.conf file
            This is needed for routing requests to the upstream

            Based on:
                part_path: path to the part containing the location
                config_path: path to the NGINX router default.conf file
        """
        path_err = "Path to location part (part_path) must be of string type"
        config_err = "Path to NGINX router file (config_path) must be of string type"

        self.str_check(part_path, path_err)
        self.str_check(config_path, config_err)
        # skip if it's not present (not an error b/c database and cache are always not present)
        if self.isfile_check(part_path) is False:
            return None
        # TODO add the actual append logic
        print('debug, trial: adding location portion for {} in file {}'.format(
            part_path, config_path))
        # read the part data and the nginx config default data
        with open(part_path, 'r') as part_file:
            part_data = part_file.readlines()
        with open(config_path, 'r') as file:
            cur_config = file.readlines()
        # delete the bracket at the end of the nginx config
        del cur_config[-1]
        # add the new content to the NGINX config at the end
        # and readd the bracket
        cur_config.extend(part_data)
        cur_config.append('}')
        # write the data to the new NGINX config file
        with open(config_path, 'w') as new_config:
            new_config.writelines(cur_config)
