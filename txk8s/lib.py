"""
Kubernetes Client done Twisted style.
"""
from os import environ

import yaml

from kubernetes import client, config

from twisted.internet import defer, reactor
from twisted.python import log


TIMEOUT = 1 # seconds


class TxKubernetesClient(object):
    """
    Wrapper for Kubernetes Python Client to make requests to the Kubernetes
    API Server asynchronous with Twisted deferreds.
    """
    def __init__(self):
        """
        Load the kube config and create an instance of the Kubernetes API client.
        """
        if environ.get('KUBERNETES_PORT'):
            config.load_incluster_config()
        else:
            config.load_kube_config()

        self.client = client
        self._apiClient = client.ApiClient()
        self.coreV1 = client.CoreV1Api(self._apiClient)
        self.rbacV1Beta1 = client.RbacAuthorizationV1beta1Api(self._apiClient)
        self.extV1Beta1 = client.ExtensionsV1beta1Api(self._apiClient)

    def __getattr__(self, attr):
        """
        Return attributes of the Kubernetes API client.
        """
        return getattr(self.client, attr)

    def call(self, apiMethod, *args, **kwargs):
        """
        Make an asynchronous request to k8s API server with twisted deferreds.
        """
        def _handleErr(fail):
            """
            Log the error and return the failure.
            """
            log.err('Error in: %s. Failure: %s.' % (apiMethod, fail))
            return fail

        d = defer.Deferred()

        # k8s python client v3 supports passing in a callback,
        # but does not handle the error case, therefore addTimeout is added to handle the case of error.
        kwargs['callback'] = d.callback
        apiMethod(*args, **kwargs)
        d.addTimeout(TIMEOUT, reactor)
        d.addErrback(_handleErr)
        return d


def createPVC(res, metadata, spec, namespace):
    """
    Create a Persistent Volume Claim kubernetes resource in a namespace.
    """
    txk8s = TxKubernetesClient()
    body = txk8s.V1PersistentVolumeClaim(
        kind='PersistentVolumeClaim',
        api_version='v1',
        metadata=metadata,
        spec=spec,
    )

    d = txk8s.call(txk8s.coreV1.create_namespaced_persistent_volume_claim,
        namespace,
        body,
    )
    return d
    

def createStorageClass(res, metadata, provisioner):
    """
    Create a Storage Class kubernetes resource.
    """
    txk8s = TxKubernetesClient()
    body = txk8s.V1beta1StorageClass(
        api_version='storage.k8s.io/v1beta1',
        kind='StorageClass',
        metadata=metadata,
        provisioner=provisioner,

    )

    storage = txk8s.StorageV1beta1Api()
    d = txk8s.call(storage.create_storage_class,
        body=body,
    )
    return d


def createDeploymentFromFile(res, filePath, namespace='default'):
    """
    Create a Deployment kubernetes resource from a yaml manifest file.
    """
    txk8s = TxKubernetesClient()

    with open(filePath, 'r') as file:
        deployment = yaml.load(file)

        d = txk8s.call(txk8s.extV1Beta1.create_namespaced_deployment,
            body=deployment,
            namespace=namespace,
        )
        return d


def createConfigMap(metadata, data, namespace):
    """
    Create a configmap kubernetes resources in a namespace.
    """
    txk8s = TxKubernetesClient()

    body = txk8s.V1ConfigMap(
        kind='ConfigMap',
        metadata=metadata,
        data=data,
    )

    d = txk8s.call(txk8s.coreV1.create_namespaced_config_map,
        namespace,
        body
    )
    return d


def createService(filePath, namespace):
    """
    Create a namespaced Service kubernetes resource from a yaml manifest file.
    """
    txk8s = TxKubernetesClient()
    
    with open(filePath, 'r') as file:
        body = yaml.load(file)

        d = txk8s.call(txk8s.coreV1.create_namespaced_service,
            namespace,
            body,
        )
        return d


def createServiceAccount(res, filePath, namespace):
    """
    Create a Service Account kubernetes resource from a yaml manifest file.
    """
    txk8s = TxKubernetesClient()
    
    with open(filePath, 'r') as file:
        body = yaml.load(file)

        d = txk8s.call(txk8s.coreV1.create_namespaced_service_account,
            namespace,
            body,
        )
        return d


def createClusterRole(res, filePath):
    """
    Create a Cluster Role kubernetes resource from a yaml manifest file.
    """
    txk8s = TxKubernetesClient()
    
    with open(filePath, 'r') as file:
        body = yaml.load(file)

        d = txk8s.call(txk8s.rbacV1Beta1.create_cluster_role,
            body,
        )
        return d


def createClusterRoleBind(res, filePath):
    """
    Create a Cluster Role Binding kubernetes resource from a yaml manifest file.
    """
    txk8s = TxKubernetesClient()
    
    with open(filePath, 'r') as file:
        body = yaml.load(file)

        d = txk8s.call(txk8s.rbacV1Beta1.create_cluster_role_binding,
            body,
        )
        return d


def createIngress(res, filePath, namespace):
    """
    Create a Ingress kubernetes resource from a yaml manifest file
    """
    txk8s = TxKubernetesClient()
    
    with open(filePath, 'r') as file:
        body = yaml.load(file)

        d = txk8s.call(txk8s.extV1Beta1.create_namespaced_ingress,
            namespace,
            body,
        )
        return d


def createEnvVar(envName, configMapName, configMapKey):
    """
    Create a environment variable kubernetes resource that references
    a value in a configmap.
    """
    txk8s = TxKubernetesClient()
    return txk8s.V1EnvVar(
        name=envName,
        value_from=txk8s.V1EnvVarSource(
            config_map_key_ref=txk8s.V1ConfigMapKeySelector(
                name=configMapName,
                key=configMapKey,
            ),
        ),
    )
