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
    allowed_frontends = ['static', 'dynamic', 'react', 'reactjs']
    allowed_backends = ['node', 'flask', 'django']
    allowed_databases = ['mongo', 'postgres', 'mysql', 'mariadb']
    allowed_caches = ['redis', 'memcached']

    def __init__(self, parts_root=None, project_name=None, front_enabled=False, back_enabled=False):
        """
            Init method for class, sets important path information
        """
        # do some checking on the config info passed
        self.str_check(
            parts_root, "root to parts directory must be of type string in PartBuilder init function")
        self.str_check(
            project_name, "default.conf file for NGINX router must be of type string in PartBuilder init function")

        nginx_file = "{}/nginx_router/nginx_conf/default.conf".format(
            project_name)
        compose_file = "{}/docker-compose.yml".format(project_name)

        if not os.path.isfile(nginx_file):
            raise PartBuilderException(
                "{} is not a file or does not exist".format(nginx_file))
        if not os.path.isfile(compose_file):
            raise PartBuilderException(
                "{} is not a file or does not exist".format(compose_file))

            # if all is good we got here without raising an exception, set instance to init info
        self.parts_root = parts_root
        self.project_name = project_name
        self.nginx_file = nginx_file
        self.compose_file = compose_file
        self.allowed_master = []
        self.allowed_master.extend(self.allowed_frontends)
        self.allowed_master.extend(self.allowed_backends)
        self.allowed_master.extend(self.allowed_databases)
        self.allowed_master.extend(self.allowed_caches)
        self.compose_router_update(
            front_enabled=front_enabled, back_enabled=back_enabled)

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

    # ---> pipeline build section <---
    def build_pipeline(self, name, pipeline, parts={}):
        """
            builds the config file for the ci / cd selected by user for the parts provided

            Based on:
                name: name of the project, used for tagging docker builds
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts for project
        """
        if (len(parts) == 0) or (parts.values() == [None for tmp in range(len(parts.values()))]):
            raise PartBuilderException(
                'PartBuilder cannot build CI/CD pipeline with no parts provided')

        parts_path = "{}/pipeline/{}".format(self.parts_root, pipeline)
        base_part_path = "{}/base.part".format(parts_path)
        config_path = None

        if pipeline == 'travis':
            config_path = "{}/.travis.yml".format(self.project_name)
        else:
            raise PartBuilderException(
                "Pipeline ({}) is not yet configured for synth!")

        # build the base of the config file for chosen CI/CD framework
        with open(base_part_path, 'r') as base_part:
            part_data = base_part.readlines()
        with open(config_path, 'w') as new_config:
            new_config.writelines(part_data)

        # build the rest of the config file
        self.build_pipeline_section_pre_tests(
            pipeline, parts, parts_path, config_path)
        self.build_pipeline_section_tests(
            pipeline, parts, parts_path, config_path)
        self.build_pipeline_section_deploy(
            pipeline, parts, parts_path, config_path)
        with open(config_path, 'r') as cur_config:
            conf_data = cur_config.readlines()
        new_data = []
        for line in conf_data:
            line = line.format(self.project_name)
            new_data.append(line)
        with open(config_path, 'w') as new_config:
            new_config.writelines(new_data)

    # should not be used outside of class
    def build_pipeline_section_pre_tests(self, pipeline, parts, parts_path, config_path):
        """
            builds the before_install section to build containers for testing

            Base on:
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts to test
                parts_path: path to pipeline parts location
                config_path: path to config file for pipeline
                             e.g: .travis.yml
        """
        # grab current config data from file so its not overwritten,
        # more efficient than constantly writing to the file with append mode in loop
        parts_path += "/pre_tests"
        config_data = []
        with open(config_path, 'r') as base_config:
            config_data = base_config.readlines()

        with open("{}/base.part".format(parts_path), 'r') as base_part:
            part_data = base_part.readlines()
            config_data.extend(part_data)

        for part_name, part in parts.items():
            # all parts passed by default, some None
            # no need to deploy/test cache or database as image is just the official image, no customizations for prod
            # also dynamic and static don't have default tests
            if part is None or part_name == "cache" or part_name == "database" or part in ['dynamic', 'static']:
                continue
            # skip if file is missing (not set up)
            # part_name is used here because not specific part files, just frontend or backend
            if not os.path.isfile("{}/{}.part".format(parts_path, part_name)):
                continue
            # do the building for before_install
            # again part_name is used due to directory name scheme
            with open("{}/{}.part".format(parts_path, part_name), 'r') as file:
                part_data = file.readlines()
                config_data.extend(part_data)

        with open(config_path, 'w') as new_config:
            new_config.writelines(config_data)

    # should not be used outside of class
    def build_pipeline_section_tests(self, pipeline, parts, parts_path, config_path):
        """
            builds the before_install section to build containers for testing

            Base on:
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts to test
                parts_path: path to pipeline parts location
                config_path: path to config file for pipeline
                             e.g: .travis.yml
        """
        # grab current config data from file so its not overwritten,
        # more efficient than constantly writing to the file with append mode in loop
        parts_path += "/tests"
        config_data = []
        with open(config_path, 'r') as base_config:
            config_data = base_config.readlines()

        with open("{}/base.part".format(parts_path), 'r') as base_part:
            part_data = base_part.readlines()
            config_data.extend(part_data)

        for part_name, part in parts.items():
            # all parts passed by default, some None
            # no need to deploy/test cache or database as image is just the official image, no customizations for prod
            if part is None or part_name == "cache" or part_name == "database":
                continue
            # skip if file is missing (not set up)
            if not os.path.isfile("{}/{}.part".format(parts_path, part)):
                continue
            # do the building for before_install
            with open("{}/{}.part".format(parts_path, part), 'r') as file:
                part_data = file.readlines()
                config_data.extend(part_data)

        with open(config_path, 'w') as new_config:
            new_config.writelines(config_data)

    # should not be used outside of class
    # TODO implement
    def build_pipeline_section_deploy(self, pipeline, parts, parts_path, config_path):
        """
            builds the before_install section to build containers for testing

            Base on:
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts to test
                parts_path: path to pipeline parts location
                config_path: path to config file for pipeline
                             e.g: .travis.yml
        """
        # grab current config data from file so its not overwritten,
        # more efficient than constantly writing to the file with append mode in loop
        parts_path += "/deploy"
        config_data = []
        with open(config_path, 'r') as base_config:
            config_data = base_config.readlines()

        with open("{}/base.part".format(parts_path), 'r') as base_part:
            part_data = base_part.readlines()
            config_data.extend(part_data)

        # add the build stage for the docker deploy
        # add the nginx router, always included
        # not included in parts dict because dict has no order
        build_dir = parts_path + "/build"
        with open("{}/router.part".format(build_dir), 'r') as router_part:
            part_data = router_part.readlines()
            config_data.extend(part_data)

        for part_name, part in parts.items():
            # all parts passed by default, some None
            # no need to deploy/test cache or database as image is just the official image, no customizations for prod
            if part is None or part_name == "cache" or part_name == "database":
                continue
            # skip if file is missing (not set up)
            if not os.path.isfile("{}/{}.part".format(build_dir, part_name)):
                continue
            # add the build stage for the part
            with open("{}/{}.part".format(build_dir, part_name), 'r') as file:
                part_data = file.readlines()
                config_data.extend(part_data)

        # add the nginx router, always included
        # not included in parts dict because dict has no order
        push_dir = parts_path + "/push"
        with open("{}/router.part".format(push_dir), 'r') as router_part:
            part_data = router_part.readlines()
            config_data.extend(part_data)
        # add the push stage for docker deploy to hub
        for part_name, part in parts.items():
            # all parts passed by default, some None
            # no need to deploy/test cache or database as image is just the official image, no customizations for prod
            if part is None or part_name == "cache" or part_name == "database":
                continue
            # skip if file is missing (not set up)
            if not os.path.isfile("{}/{}.part".format(push_dir, part_name)):
                continue
            with open("{}/{}.part".format(push_dir, part_name), 'r') as file:
                part_data = file.readlines()
                config_data.extend(part_data)

        with open(config_path, 'w') as new_config:
            new_config.writelines(config_data)

    # ---> nginx and compose build section <---
    def add_part(self, part=None, database=None, cache=None):
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
            # build the NGINX router default.conf
            self.upstream_add(self.parts_root +
                              '/nginx/upstream/{}.part'.format(part), self.nginx_file)
            self.location_add(self.parts_root +
                              '/nginx/location/{}.part'.format(part), self.nginx_file)

            # build the docker-compose file
            self.compose_add(self.parts_root +
                             '/compose/{}.part'.format(part), self.compose_file)
            if part in self.allowed_backends and (database is not None or cache is not None):
                self.backend_compose_update(database, cache)

        else:
            raise PartBuilderException(
                "part provided to PartBuilder ({}) is not in allowed_master".format(part))

    def compose_router_update(self, front_enabled=False, back_enabled=False):
        """
        must be run before all other things dealing with compose building
        due to relating with the router
        """
        if not front_enabled and not back_enabled:
            return
        self.compose_add(
            self.parts_root + '/compose/depends/base.part',
            self.compose_file)
        if front_enabled:
            self.compose_add(
                self.parts_root + '/compose/depends/frontend.part',
                self.compose_file
            )
        if back_enabled:
            self.compose_add(
                self.parts_root + '/compose/depends/backend.part',
                self.compose_file
            )

    def backend_compose_update(self, database, cache):
        """
            updates the compose file after adding a part if its a backend by adding
            neccessary environmental variables and depends_on sections
        """
        if (database not in self.allowed_databases and cache not in self.allowed_caches):
            raise PartBuilderException(
                "backend_compose_update failed because database or cache not in allowed services"
            )
        self.compose_add(
            self.parts_root + '/compose/depends/base.part',
            self.compose_file)
        if database in self.allowed_databases:
            self.compose_add(
                self.parts_root +
                '/compose/depends/{}.part'.format(database),
                self.compose_file
            )
        if cache in self.allowed_caches:
            self.compose_add(
                self.parts_root +
                '/compose/depends/{}.part'.format(cache),
                self.compose_file
            )
        # add environment variables for cache and database
        self.compose_add(
            self.parts_root + '/compose/env/base.part',
            self.compose_file
        )
        if database in self.allowed_databases:
            self.compose_add(
                self.parts_root +
                '/compose/env/{}.part'.format(database),
                self.compose_file
            )
        if cache in self.allowed_caches:
            self.compose_add(
                self.parts_root +
                '/compose/env/{}.part'.format(cache),
                self.compose_file
            )

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
        if os.path.isfile(part_path) is False:
            raise PartBuilderException(
                "{} is not a file or did not exist.".format(part_path))
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
        if os.path.isfile(part_path) is False:
            return None
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
        if os.path.isfile(part_path) is False:
            return None
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
