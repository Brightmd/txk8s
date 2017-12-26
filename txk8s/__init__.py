"""
Twisted implementation for Kubernetes
"""

from txk8s import _version
from txk8s.lib import (TxKubernetesClient,
                  createPVC,
                  createStorageClass,
                  createDeploymentFromFile,
                  createConfigMap,
                  createService,
                  createServiceAccount,
                  createClusterRole,
                  createClusterRoleBind,
                  createIngress,
                  createEnvVar,)

(_version,
 TxKubernetesClient,
 createPVC,
 createStorageClass,
 createDeploymentFromFile,
 createConfigMap,
 createService,
 createServiceAccount,
 createClusterRole,
 createClusterRoleBind,
 createIngress,
 createEnvVar,) # for pyflakes
