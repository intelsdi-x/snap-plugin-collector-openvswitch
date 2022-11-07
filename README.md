DISCONTINUATION OF PROJECT. 

This project will no longer be maintained by Intel.

This project has been identified as having known security escapes.

Intel has ceased development and contributions including, but not limited to, maintenance, bug fixes, new releases, or updates, to this project.  

Intel no longer accepts patches to this project.
# Snap collector plugin - OpenVswitch
This Snap plugin collects metrics from the OpenVswitch software switch. 

It's used in the [Snap framework](http://github.com/intelsdi-x/snap).

1. [Getting Started](#getting-started)
  * [System Requirements](#system-requirements)
  * [Operating systems](#operating-systems)
  * [Installation](#installation)
  * [Configuration and Usage](#configuration-and-usage)
2. [Documentation](#documentation)
  * [Collected Metrics](#collected-metrics)
  * [Examples](#examples)
  * [Roadmap](#roadmap)
3. [Community Support](#community-support)
4. [Contributing](#contributing)
5. [License](#license)

## Getting Started
### System Requirements
* [python 2.7+](https://www.python.org/downloads/)
* [pyenv 1.0.10+](https://github.com/pyenv/pyenv)
* [acbuild 0.4.0+](https://github.com/containers/build)
    The acbuild tool will be downloaded automatically while building ACI package, but it is recommended to install it manually in your system to speed up build process. For Ubuntu, you can do it just by:

    ```
    sudo apt-get install acbuild
    ```

For testing:
* [tox](https://tox.readthedocs.io/en/latest/) (install using `pip install tox`)

### Operating systems
The plugin should work on any platform with Python2.7.  The plugin has been tested on Linux and FreeBSD.

### Installation
#### Python module

The preferred way to run Python based plugins is to leverage the python package
index.  This means that the Snap daemon, *snapteld*, will need to be run in an
environment where the python module `snap-plugin-collector-openvswitch` was installed.
If you install the plugin (`pip install snap-plugin-collector-openvswitch`) into the
system's Python environment that should be enough.  If you use a
[virtualenv](https://pypi.python.org/pypi/virtualenv) be sure to activate it
before starting `snapteld` since it will need access to the plugin and its
dependencies.

To install the plugin run:
* `pip install snap-plugin-collector-openvswitch`

The plugin includes a command line entry point also called
`snap-plugin-collector-openvswitch` which should be in your path after installation.

Find the plugin's command line script:
* `which snap-plugin-collector-openvswitch`

```
which snap-plugin-collector-openvswitch
> /home/mspoczy/.pyenv/versions/py2712/bin/snap-plugin-collector-openvswitch
```

The entry point script, snap-plugin-collector-openvswitch, is what we will be
load into `snapteld` with the following command.

```
snaptel plugin load `which snap-plugin-collector-openvswitch`
```

#### Plugin package

An alternative installation method for Linux X86_64 is to use the binary package.
The package includes a Python 2.7 distribution with the plugin already installed.

You can get the pre-built plugin package under
[releases](https://github.com/intelsdi-x/snap-plugin-collector-openvswitch/releases)
page.

Known issues:
* Longer plugin load times
* A package is only available for Linux X86_64

Since the current default timeout may be exceeded start `snapteld` with the flag
`--plugin-load-timeout 30` (e.g. `snapteld -t 0 -1 --plugin-load-timeout 30`).
Lastly, when you load the plugin you will also want to increase the clients
timeout using the flag `--timeout 30s` (e.g. `snaptel --timeout 30s plugin load snap-plugin-collector-openvswitch`).

### Configuration and Usage
* Start snapteld
  * See the Snap [readme](https://github.com/intelsdi-x/snap/blob/master/README.md#getting-started) for getting started details
  * Start snap: `snapteld -t 0 -l 1`
* Ensure that openvswitch is **installed** and **enabled**

## Documentation
### Collected Metrics
This plugin will identify all the interfaces and bridges connected to the OpenVswitch.

Below is an example of the metrics being gathered from OpenVswitch 2.6


Namespace | Data Type | Description (optional)
----------|-----------|-----------------------
/intel/ovs/$deviceName/rx_over_err | int |
/intel/ovs/$deviceName/tx_dropped | int |
/intel/ovs/$deviceName/rx_packets | int |
/intel/ovs/$deviceName/rx_frame_err | int |
/intel/ovs/$deviceName/rx_bytes | int |
/intel/ovs/$deviceName/tx_errors | int |
/intel/ovs/$deviceName/rx_crc_err | int |
/intel/ovs/$deviceName/collisions | int |
/intel/ovs/$deviceName/rx_errors | int |
/intel/ovs/$deviceName/tx_bytes | int |
/intel/ovs/$deviceName/rx_dropped | int |
/intel/ovs/$deviceName/tx_packets | int |

### Examples
In this example we will collect data from OpenVswitch and publish it to a file. It is assumed that you are using the latest Snap binary and plugins.

The example is run from a directory which includes snaptel, snapteld, along with the plugins and task file.

21 Start the Snap daemon:

  * Run:

  ```
  $ snapteld -l 1 -t 0
  ```

  The option "-l 1" is for setting the debugging log level and "-t 0" is for disabling plugin signing.

2.  Load the plugin:

  * Run (in a different terminal):

```
$ snaptel plugin load `which snap-plugin-collector-openvswitch`
Plugin loaded
Name: openvswitchcollectorplugin-py
Version: 1
Type: collector
Signed: false
Loaded Time: Fri, 19 Jan 2018 16:57:35 PDT
```

##### Load from ACI package:

If using ACI package, you don't need to pass any environment variables, just start Snap daemon with root permissions:
```
$ sudo snapteld -l 1 -t 0
```

Then load openvswitch plugin from ACI package:
```
$ snaptel plugin load dist/snap-plugin-collector-openvswitch/linux/x86_64/snap-plugin-collector-openvswitch-linux-x86_64.aci
Plugin loaded
Name: openvswitchcollectorplugin-py
Version: 1
Type: collector
Signed: false
Loaded Time: Fri, 19 Jan 2018 11:20:05 PDT
```

  * List the metric catalog by running:

```
$ snaptel metric list
NAMESPACE 				 VERSIONS
/intel/ovs/*/rx_over_err   1
/intel/ovs/*/tx_dropped   1
/intel/ovs/*/rx_packets   1
/intel/ovs/*/rx_frame_err   1
/intel/ovs/*/rx_bytes   1
/intel/ovs/*/tx_errors   1
/intel/ovs/*/rx_crc_err   1
/intel/ovs/*/collisions   1
/intel/ovs/*/rx_errors   1
/intel/ovs/*/tx_bytes   1
/intel/ovs/*/rx_dropped   1
/intel/ovs/*/tx_packets   1
```

  See available metrics for your system. Note the `*` in the metric list.  It
  indicates a dynamic metric which will be update depending on the device names
  and attribute available on the system being monitored.

4.  Download the file publisher plugin and load it

  *  Get the latest file publisher plugin by running:

```
$ wget  http://snap.ci.snap-telemetry.io/plugins/snap-plugin-publisher-file/latest/linux/x86_64/snap-plugin-publisher-file
```

  * Load the file publisher plugin by running:

```
$ snaptel plugin load snap-plugin-publisher-file
Plugin loaded
Name: file
Version: 2
Type: publisher
Signed: false
Loaded Time: Fri, 19 Jan 2018 14:47:59 PDT
```

  * Create a task file by running:

```
cat <<EOF>ovs-file.yaml
---
  version: 1
  schedule:
    type: "simple"
    interval: "1s"
  workflow:
    collect:
      metrics:
        /intel/ovs/*/rx_over_err: {}
        /intel/ovs/*/tx_dropped: {}
        /intel/ovs/*/rx_packets: {}
        /intel/ovs/*/rx_frame_err: {}
        /intel/ovs/*/rx_bytes: {}
        /intel/ovs/*/tx_errors: {}
        /intel/ovs/*/rx_crc_err: {}
        /intel/ovs/*/collisions: {}
        /intel/ovs/*/rx_errors: {}
        /intel/ovs/*/tx_bytes: {}
        /intel/ovs/*/rx_dropped: {}
        /intel/ovs/*/tx_packets: {}
      publish:
        -
          plugin_name: file
          config:
            file: /tmp/published_ovs.out
EOF
```

  [Example (JSON) task manifest](https://github.com/intelsdi-x/snap-plugin-collector-openvswitch/blob/master/examples/tasks/ovs-file.json)

5.  Start task by running:
```
$ snaptel task create -t ovs-file.yaml
Using task manifest to create task
Task created
ID: c6d095a6-733d-40cf-a986-9c82aa64b4e2
Name: Task-c6d095a6-733d-40cf-a986-9c82aa64b4e2
State: Running
```

  * List the task by running:
```
$ snaptel task list
ID 					 NAME 						 STATE 		 HIT 	 MISS 	 FAIL 	 CREATED 		 LAST FAILURE
c6d095a6-733d-40cf-a986-9c82aa64b4e2 	 Task-c6d095a6-733d-40cf-a986-9c82aa64b4e2 	 Running 	 9 	 0 	 0 	 10:39AM 2-23-2017
```

  * Watch the task by running:
```
$ snaptel task watch c6d095a6-733d-40cf-a986-9c82aa64b4e2
```

  * Stop the task by running:
```
$ snaptel task stop c6d095a6-733d-40cf-a986-9c82aa64b4e2
Task stopped:
ID: c6d095a6-733d-40cf-a986-9c82aa64b4e2
```

### Roadmap
There isn't a current roadmap for this plugin, but it is in active development. As we launch this plugin, we do not have any outstanding requirements for the next release. If you have a feature request, please add it as an [issue](https://github.com/intelsdi-x/snap-plugin-collector-openvswitch/issues/new) and/or submit a [pull request](https://github.com/intelsdi-x/snap-plugin-collector-openvswitch/pulls).

## Community Support
This repository is one of **many** plugins in **Snap**, a powerful telemetry framework. See the full project at http://github.com/intelsdi-x/snap To reach out to other users, head to the [main framework](https://github.com/intelsdi-x/snap#community-support)

## Contributing
We love contributions!

There's more than one way to give back, from examples to blogs to code updates. See our recommended process in [CONTRIBUTING.md](CONTRIBUTING.md).

## License
[Snap](http://github.com/intelsdi-x/snap), along with this plugin, is an Open Source software released under the Apache 2.0 [License](LICENSE).

* Author: [Marcin Spoczynski](https://github.com/sandlbn/)

This software has been contributed by MIKELANGELO, a Horizon 2020 project co-funded by the European Union. https://www.mikelangelo-project.eu/
## Thank You

And **thank you!** Your contribution, through code and participation, is incredibly important to us.
