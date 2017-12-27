"""
Twisted implementation for Kubernetes
"""

from txk8s._version import __version__
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

(__version__,
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
