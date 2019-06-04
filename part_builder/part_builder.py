#!/usr/bin/env python3
"""
    Builds the docker-compose file using modular
    components specified by the user

    Also builds the NGINX router default.conf
    containing the routing for desired services

    Functions primarily do text appending,
    CLI logic is enclosed in synth.py
"""
from part_builder import PartBuilderException


class PartBuilder():
    """
        Part builder class for use with building the compose file
        and nginx router file
    """
    allowed_frontends = ['static', 'node', 'react', 'reactjs']
    allowed_backends = ['node', 'flask', 'django']
    allowed_databases = ['mongo', 'postgres', 'mysql']
    # TODO not yet implemented
    # allowed_caches = ['redis', 'memcache']

    def __init__(self, parts_root=None, nginx_root=None, compose_root=None):
        """
            Init method for class, sets important path information
        """
        # should be the path ending in /parts (parts directory)
        self.parts_root = parts_root
        self.nginx_root = nginx_root
        self.compose_root = compose_root

    def add_frontend(self, frontend=None):
        """
            adds a frontend based on a string passed

            Based on:
                frontend: string representing frontend,
                    e.g: static
        """
        self.none_check(frontend, "Cannot add frontend of None")
        frontend = frontend.lower()
        # append neccessary content for the frontend to the compose and nginx config files
        if frontend in self.allowed_frontends:
            compose_add(self.parts_root +
                        '/compose/{}.part'.format(frontend), self.compose_root)
            upstream_add(
                self.parts_root + '/nginx/upstream/{}.part'.format(frontend), self.nginx_root)
            location_add(
                self.parts_root + '/nginx/location/{}.part'.format(frontend), self.nginx_root)
        else:
            raise PartBuilderException(
                "Frontend provided to PartsBuilder not in allowed frontends")

    @staticmethod
    def none_check(param=None, err_msg="Path Error"):
        """
            Checks that variables passed to PartBuilder functions
            are not None and exist

            Based on:
                param: variable to check
                err_msg: error message to output
        """
        if param is None:
            raise PartBuilderException(err_msg)

    def compose_add(self, part_path=None, config_path=None):
        """
            Adds a part to the master docker-compose file

            Based on:
                part_path: path to the part to add
                compose_path: path to master compose file to add to
        """
        path_err = "Path to compose service part (part_path) can't be None"
        config_err = "Path to docker-compose file (config_path) can't be None"

        self.none_check(part_path, path_err)
        self.none_check(config_path, config_err)

    def upstream_add(self, part_path=None, config_path=None):
        """
            Adds an upstream to the NGINX router default.conf file

            Based on:
                part_path: path to the part containing the upstream
                config_path: path to the NGINX router default.conf file
        """
        path_err = "Path to upstream part (part_path) can't be None"
        config_err = "Path to NGINX router file (config_path) can't be None"

        self.none_check(part_path, path_err)
        self.none_check(config_path, config_err)

    def location_add(self, part_path=None, config_path=None):
        """
            Adds a location block to the server block in the NGINX router
            default.conf file
            This is needed for routing requests to the upstream

            Based on:
                part_path: path to the part containing the location
                config_path: path to the NGINX router default.conf file
        """
        path_err = "Path to location part (part_path) can't be None"
        config_err = "Path to NGINX router file (config_path) can't be None"

        self.none_check(part_path, path_err)
        self.none_check(config_path, config_err)
