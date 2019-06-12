![synth logo](assets/logo.png)

# synth - a Docker bootstrapping tool

Inspired by how long it can take to set up the development of web apps, synth is a tool to help you build modular sets of Docker files, Docker Compose files, directory trees, and wireframed files for different web frameworks. synth can help you set up your next web application project in seconds, allowing you to start coding your idea with zero hassle.

## :running: Getting Started

* [Ubuntu 14.04 LTS](http://releases.ubuntu.com/14.04/) - Operating system reqd.

* [Python 3.4](https://www.python.org/downloads/release/python-340/) - Python version used

* [Node.js 12.3.1](https://nodejs.org/en/download/current/) - Node version used

## :warning: Dependencies

* `docker` and `docker-compose`

* `python3`

## :arrow_down: Installation

Clone the repository into a new directory

```
$ git clone https://github.com/BennettDixon/synth.git
```

Run the installer script

```
./install.sh
```

## Usage

```
synth [OPTIONS]
```

## Options

```
--frontend
```

Your frontend framework. Currently supported options are `static`, `dynamic`, `react`.

```
--backend
```

Your backend framework. Currently supported options are `flask`, `node`, `django`.

```
--database
```

Your choice of database. Currently supported options are `mysql`, `postgres`, `mongo`.

```
--cache
```

Your choice of caching tool. Currently supported options are `redis` and `memcache`.

## :books: Coding Style Tests

Strictly followed `pep8` style guide. To install

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

* 0.1.0

## Contributing

See [CONTRIBUTING.md]

## :blue_book: Authors
* **Bennett Dixon** - [@BennettDixon](https://github.com/BennettDixon)
* **Jack Gindi** - [@jmgindi](https://github.com/jmgindi)

## :mag: License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## :mega: Acknowledgments

* [Holberton School](https://github.com/holbertonschool) (providing guidance)

* [Julian Gindi](https://github.com/JulianGindi) (project mentor)