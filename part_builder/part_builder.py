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

    @classmethod
    def check_paths(cls, part_path, config_path, path_err="Path Error", config_err="Config Error"):
        """
            Checks that variables passed to PartBuilder functions
            are not None and exist

            Based on:
                part_path: path to check
                config_path: path to check
                path_err: error to output if part_path is None
                config_err: error to output if config_path is None
        """
        if part_path is None:
            raise PartBuilderException(path_err)
        if config_path is None:
            raise PartBuilderException(config_err)

    @classmethod
    def compose_add(cls, part_path=None, config_path=None):
        """
            Adds a part to the master docker-compose file

            Based on:
                part_path: path to the part to add
                compose_path: path to master compose file to add to
        """
        path_err = "Path to compose service part (part_path) can't be None"
        config_err = "Path to docker-compose file (config_path) can't be None"

        cls.check_paths(part_path, config_path, path_err, config_err)

    @classmethod
    def upstream_add(cls, part_path=None, config_path=None):
        """
            Adds an upstream to the NGINX router default.conf file

            Based on:
                part_path: path to the part containing the upstream
                config_path: path to the NGINX router default.conf file
        """
        path_err = "Path to upstream part (part_path) can't be None"
        config_err = "Path to NGINX router file (config_path) can't be None"

        cls.check_paths(part_path, config_path, path_err, config_err)

    @classmethod
    def location_add(cls, part_path=None, config_path=None):
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

        cls.check_paths(part_path, config_path, path_err, config_err)
