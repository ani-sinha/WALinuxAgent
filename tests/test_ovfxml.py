# Copyright 2014 Microsoft Corporation
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
#
# Requires Python 2.4+ and Openssl 1.0+
#
# Implements parts of RFC 2131, 1541, 1497 and
# http://msdn.microsoft.com/en-us/library/cc227282%28PROT.10%29.aspx
# http://msdn.microsoft.com/en-us/library/cc227259%28PROT.13%29.aspx

import env
import tests.tools as tools
import uuid
import unittest
import os
import json
import azureguestagent.protocol.v1 as v1

ExtensionsConfigSample="""
 <Environment xmlns="http://schemas.dmtf.org/ovf/environment/1" xmlns:oe="http://schemas.dmtf.org/ovf/environment/1" xmlns:wa="http://schemas.microsoft.com/windowsazure" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <wa:ProvisioningSection>
      <wa:Version>1.0</wa:Version>
      <LinuxProvisioningConfigurationSet xmlns="http://schemas.microsoft.com/windowsazure" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <ConfigurationSetType>LinuxProvisioningConfiguration</ConfigurationSetType>
        <HostName>HostName</HostName>
        <UserName>UserName</UserName>
        <UserPassword>UserPassword</UserPassword>
        <DisableSshPasswordAuthentication>false</DisableSshPasswordAuthentication>
        <SSH>
          <PublicKeys>
            <PublicKey>
              <Fingerprint>EB0C0AB4B2D5FC35F2F0658D19F44C8283E2DD62</Fingerprint>
              <Path>$HOME/UserName/.ssh/authorized_keys</Path>
            </PublicKey>
          </PublicKeys>
          <KeyPairs>
            <KeyPair>
              <Fingerprint>EB0C0AB4B2D5FC35F2F0658D19F44C8283E2DD62</Fingerprint>
              <Path>$HOME/UserName/.ssh/id_rsa</Path>
            </KeyPair>
          </KeyPairs>
        </SSH>
        <CustomData>CustomData</CustomData>
      </LinuxProvisioningConfigurationSet>
    </wa:ProvisioningSection>
 </Environment>
"""

class TestOvf(unittest.TestCase):
    def test_ovf(self):
        config = v1.OvfEnv(ExtensionsConfigSample)
        self.assertEquals(1, config.getMajorVersion())
        self.assertEquals(0, config.getMinorVersion())
        self.assertEquals("HostName", config.getComputerName())
        self.assertEquals("UserName", config.getUserName())
        self.assertEquals("UserPassword", config.getUserPassword())
        self.assertEquals(False, config.getDisableSshPasswordAuthentication())
        self.assertEquals("CustomData", config.getCustomData())
        self.assertNotEquals(None, config.getSshPublicKeys())
        self.assertEquals(1, len(config.getSshPublicKeys()))
        self.assertNotEquals(None, config.getSshKeyPairs())
        self.assertEquals(1, len(config.getSshKeyPairs()))
        
if __name__ == '__main__':
    unittest.main()
