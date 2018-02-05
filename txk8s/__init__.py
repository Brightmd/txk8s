"""
Twisted implementation for Kubernetes
"""

from txk8s._version import __version__
from txk8s.lib import (TxKubernetesClient,
                  TxKubernetesError,
                  createPVC,
                  createStorageClass,
                  createDeploymentFromFile,
                  createConfigMap,
                  createService,
                  createServiceAccount,
                  createClusterRole,
                  createClusterRoleBind,
                  createIngress,
                  createEnvVar,
                  deleteConfigMap,
                  deleteDeploy,
                  deleteIngress,
                  deleteNamespace,
                  deletePVC,
                  deleteService,
                  deleteServiceAcct,
                  listDeployments,
)

(__version__,
 TxKubernetesClient,
 TxKubernetesError,
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
