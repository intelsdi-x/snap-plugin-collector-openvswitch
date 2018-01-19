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

import unittest
import mock
import json

import snap_plugin.v1 as snap
from snap_ovs import Ovs, get_switch_topology

topology_json = open("tests/test_topology.json").read()
topology = json.loads(topology_json)


class OvsTestCase(unittest.TestCase):

    # mock the DeviceList attribute in
    @mock.patch('snap_ovs.get_switch_topology', return_value=topology)
    def test_ovs_collect(self, test_topology):
        plugin = Ovs("ovs", 1)
        
        metrics = plugin.collect([
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="ovs"),
                    snap.NamespaceElement(value="*"),
                    snap.NamespaceElement(value="tx_bytes")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="ovs"),
                    snap.NamespaceElement(value="*"),
                    snap.NamespaceElement(value="rx_bytes")]),
                ])
        assert len(metrics) > 0

    def test_ovs_get_config(self):
        plugin = Ovs("ovs", 1)
        policy = plugin.get_config_policy()
        assert isinstance(policy, snap.config_policy.ConfigPolicy)

    def test_ovs_update(self):
        plugin = Ovs("ovs", 1)
        policy = plugin.get_config_policy()
        catalog = plugin.update_catalog(policy)
        assert len(catalog) == 12

