![synth logo](assets/synth_logo.png)

# synth - a Docker bootstrapping tool

Read more about the creation of synth [here](https://medium.com/@jackgindi/the-making-of-synth-4045b1a746f4)

Inspired by how long it can take to set up the development of web apps, synth is a tool to help you build modular sets of Docker, Docker Compose, and CI/CD pipeline config files, as well as directory trees and wireframed files for different front- and backend web frameworks. synth can help you set up your next web application project in seconds, allowing you to start coding your idea with zero hassle.

## :warning: Dependencies

- `docker` and `docker-compose`

- `python3`

## :arrow_down: Installation

Install via pip:

```
pip3 install boot-synth
```

## :triangular_flag_on_post: Usage

```
synth create [OPTIONS]
```

![synth demo](assets/synth_basic_demo.gif)

## :hammer_and_wrench: Options

```
--frontend, -f
```

Your frontend framework. Currently supported options are `static`, `dynamic`, `react`.

```
--backend, -b
```

Your backend framework. Currently supported options are `flask`, `node`, `django`.

```
--database, -d
```

Your choice of database. Currently supported options are `mysql`, `postgres`, `mongo`, `mariadb`.

```
--cache, -c
```

Your choice of caching tool. Currently supported options are `redis` and `memcache`.

```
--pipeline, -p
```

Your choice of CI/CD pipeline. `travis` is currently the only supported option.

## :books: Coding Style Tests

Strictly followed `pep8` style guide. To install:

### Regular Ubuntu 14.04 install

With apt-get

```
$ sudo apt-get install python3-pep8
```

With pip3

```
$ pip3 install pep8
```

### Check The Version

```
$ pep8 --version
1.7.1
```

## :pencil: Version

- 1.1.0

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## :blue_book: Authors

- **Bennett Dixon** - [@BennettDixon](https://github.com/BennettDixon) - [Portfolio](https://bencodesit.com)
- **Jack Gindi** - [@jmgindi](https://github.com/jmgindi) - [Portfolio](https://jackgindi.com)

## :mag: License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details

## :mega: Acknowledgments

- [Holberton School](https://github.com/holbertonschool) (providing guidance)

- [Julian Gindi](https://github.com/JulianGindi) (project mentor)
