#!/usr/bin/env python

# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import time
import sys

import snap_plugin.v1 as snap
from shutilwhich import which
import json
import subprocess

LOG = logging.getLogger(__name__)

metrics_table = ['rx_over_err', 'tx_dropped', 'rx_packets', 'rx_frame_err', 'rx_bytes', 'tx_errors',
           'rx_crc_err', 'collisions',  'rx_errors', 'tx_bytes', 'rx_dropped', 'tx_packets']

class Ovs(snap.Collector):
    """
    Ovs collector class
    """
    def __init__(self, *args, **kwargs):
        super(Ovs, self).__init__(*args)

    def update_catalog(self, config):
        """
        Updates snap catalog

        @param config: snap config instance
        @return: list of metrics
        """
        LOG.debug("GetMetricTypes called")
        metrics = []
        for i in metrics_table:
            metric = snap.Metric(version=self.meta.version,
                                 Description="OVS list of dynamic devices")
            metric.namespace.add_static_element("intel")
            metric.namespace.add_static_element("ovs")
            metric.namespace.add_dynamic_element("device", "device name")
            metric.namespace.add_static_element(i)
            metrics.append(metric)
        return metrics

    def get_config_policy(self):
        """
        Creates snap plugin policy
        @return: snap policy
        """
        LOG.debug("GetConfigPolicy called")
        return snap.ConfigPolicy()

    def collect(self, metrics):
        """
        Collects metrics
        @param metrics: list of snap metric namespaces
        @return: list of metrics
        """
        metrics_to_return = []
        ts_now = time.time()
        topology = get_switch_topology()
        interfaces = get_interfaces(topology)
        for iface in interfaces:
            for metric in metrics:
                tmp_metric = snap.Metric(
                    namespace=[i for i in metric.namespace],
                    unit=metric.unit)
                tmp_metric.tags = [(k, v) for k, v in metric.tags.items()]
                tmp_metric.namespace[2].value = iface[0]
                data = iface[1].get(metric.namespace[3].value, None)
                if not data:
                    continue
                tmp_metric.timestamp = ts_now
                metrics_to_return.append(metric)
        return metrics_to_return

def get_switch_topology():
    """
    Retrieving openvswitch switch topology
    @return: openvswitch list of interfaces
    """
    command = \
            "ovsdb-client -v transact '[\"Open_vSwitch\", {\"op\" : \"select\", \"table\" : \"Interfaces\", \"where\": []}]'"
    stdout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = ''.join(stdout.stdout.readlines())
    if stdout.wait() != 0:
        return ""
    return json.loads(output)


def format_ovsdb_response(port):
    """
    Parses port data
    @param port: port name
    @return: dictonary of mesurments
    """
    return dict((m[0], m[1]) for m in port[1])


def get_interfaces(topology):
    """
    Retrieving list of interfaces from ovs topology
    @param topology: openvswitch topology
    @return: list of ports
    """
    ports = []
    for row in topology[0]["rows"]:
        statistics = row.get("statistics", None)
        name = row.get("name", None)
        if name and statistics:
            port = [name, format_ovsdb_response(statistics)]
            ports.append(port)
    return ports

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
