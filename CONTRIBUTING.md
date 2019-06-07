# Reporting Issues

If you're having issues with synth, we will do what we can to try and fix it! And in case we have, try updating first.

If you've updated and are still having issues, feel free to open a GitHub issue with the following information:

* output of `synth --version`
* your system (Ubuntu, Debian, ArchLinux)
* steps to reproduce the bug
* anything else you think is relevant

# Make a pull request

We will gladly review pull requests to our code for new features, bug fixes, etc.

# Developing

Clone the repository but *do not* run the `install.sh` script

run unittests

```
python3 -m unittest discover tests
```

## .part files

.part files have a specific format:

* all docker-compose parts that set environmental variables or add depends_on functionality should be added to `synth/projects_master/parts/compose/[env/depends_on]`

* all nginx .part files should be added to `synth/projects_master/parts/nginx/[name of project]`

* .part files should include the correct levels of indentation. This means:
    - each line in any docker-compose .part file must have a minimum of 2 spaces at the beginning
    - location blocks for nginx .part files must have minimum of one tab character at the beginning of each line
