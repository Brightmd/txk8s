"""
Tests for osteoblaster's twisted kubernetes module.
"""
from builtins import str

import pytest

from builtins import str

from kubernetes import client

try: # pragma: nocover
    # python 3
    from unittest.mock import Mock, mock_open, patch
    patch_open = lambda f: patch("builtins.open", mock_open(read_data=f))
except ImportError: # pragma: nocover
    # python 2
    from mock import Mock, mock_open, patch
    patch_open = lambda f: patch("__builtin__.open", mock_open(read_data=f))

from txk8s import lib


def test_initClient(txclient):
    """
    Do I initialize with the correct attributes?
    """
    for attr in ("client", "_apiClient", "coreV1"):
        assert getattr(txclient, attr)


def test_initClientInCluster(txclientInCluster):
    """
    Do I initialize with the correct attributes?
    """
    for attr in ("client", "_apiClient", "coreV1"):
        assert getattr(txclientInCluster, attr)


def test_getAttr(txclient):
    """
    Do I get attributes from the k8s python api client?
    """
    expected = "<class 'kubernetes.client.models.v1_namespace.V1Namespace'>"
    assert str(txclient.__getattr__("V1Namespace")) == expected


@pytest.inlineCallbacks
def test_clientCallSuccess(kubeConfig):
    """
    Check that the `call` method does the following when successful:
    - adds callback to the kwargs passed to the apiMethod
    - calls the apiMethod it is passed
    - does not call the errback handler when successful
    - returns a deferred
    """
    def fakeReadNamespaceSecret(callback):
        callback('happy')
        return

    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            read_namespaced_secret=fakeReadNamespaceSecret,
        ),
        autospec=True,
    )

    with pApiMethod as mApiMethod:
        txclient = lib.TxKubernetesClient()
        res = yield txclient.call(txclient.coreV1.read_namespaced_secret)
        assert mApiMethod.call_count == 1
        assert 'happy' == res


@pytest.inlineCallbacks
def test_clientCallError(kubeConfig):
    """
    Check that the `call` method does the following when unsuccessful:
    - when the timeout is triggered the errback is triggered which logs the message about the failure
    """
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            read_namespaced_secret=Mock(),
        ),
        autospec=True,
    )
    pTimeout = patch.object(lib, 'TIMEOUT', 0)

    with pApiMethod, pTimeout:
        txclient = lib.TxKubernetesClient()
        d = txclient.call(txclient.coreV1.read_namespaced_secret)
        def _check(fail):
            assert type(fail.value) == lib.TxKubernetesError
        d.addErrback(_check)
        yield d


@pytest.inlineCallbacks
def test_deleteService(kubeConfig):
    """
    Do I delete a service kubernetes resource in a namespace?
    """
    namespace = 'test-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(lib.client,
        'CoreV1Api',
        return_value=Mock(
            delete_namespaced_service='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall:
        yield lib.deleteService('name', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_deleteSvcAcct(kubeConfig):
    """
    Do I delete a service account kubernetes resource in a namespace?
    """
    namespace = 'test-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(lib.client,
        'CoreV1Api',
        return_value=Mock(
            delete_namespaced_service_account='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall:
        yield lib.deleteServiceAcct('name', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_deleteDeploy(kubeConfig):
    """
    Do I delete a deployment kubernetes resource in a namespace?
    """
    namespace = 'test-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(lib.client,
        'ExtensionsV1beta1Api',
        return_value=Mock(
            delete_namespaced_deployment='',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall:
        yield lib.deleteDeploy('name', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_deleteIngress(kubeConfig):
    """
    Do I delete a ingress kubernetes resource in a namespace?
    """
    namespace = 'test-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(lib.client,
        'ExtensionsV1beta1Api',
        return_value=Mock(
            delete_namespaced_ingress='',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall:
        yield lib.deleteIngress('name', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_deletePVC(kubeConfig):
    """
    Do I delete a persistent volume claim kubernetes resource in a namespace?
    """
    namespace = 'test-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(lib.client,
        'CoreV1Api',
        return_value=Mock(
            delete_namespaced_persistent_volume_claim='',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall:
        yield lib.deletePVC('name', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_deleteCM(kubeConfig):
    """
    Do I delete a config map kubernetes resource in a namespace?
    """
    namespace = 'test-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(lib.client,
        'CoreV1Api',
        return_value=Mock(
            delete_namespaced_config_map='',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall:

        yield lib.deleteConfigMap('name', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_deleteNs(kubeConfig):
    """
    Do I delete a namespace kubernetes resource in a namespace?
    """
    namespace = 'test-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(lib.client,
        'CoreV1Api',
        return_value=Mock(
            delete_namespace='',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall:

        yield lib.deleteNamespace(namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_listDeployments(kubeConfig):
    """
    Do I list all the deployments in a namespace?
    """
    namespace = 'test-se-com'
    pApiMethod = patch.object(lib.client,
        'AppsV1beta1Api',
        return_value=Mock(
            list_namespaced_deployment=Mock(),
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod:
        yield lib.listDeployments(namespace)
        mApiMethod.assert_called_once()


@pytest.inlineCallbacks
def test_createPVC(kubeConfig):
    """
    Do I create a Persistent Volume Claim kubernetes resource in a namespace?
    """
    meta = 'happy'
    spec = 'days'
    namespace = 'grn-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pPVC = patch.object(client, 'V1PersistentVolumeClaim')
    pApiMethod = patch.object(client,'CoreV1Api')
    with pPVC as mPVC, pApiMethod, pCall as mCall:
        yield lib.createPVC(meta, spec, namespace)
        mPVC.assert_called_once_with(api_version='v1', kind='PersistentVolumeClaim', metadata=meta, spec=spec)
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_createStorageClass(kubeConfig):
    """
    Do I create a Storage Class kubernetes resource?
    """
    meta = 'happy'
    provisioner = 'aws-efs'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pStorage = patch.object(client, 'V1beta1StorageClass')
    pApiMethod = patch.object(client,'StorageV1beta1Api')
    with pStorage as mStorage, pApiMethod, pCall as mCall:
        yield lib.createStorageClass(meta, provisioner)
        mStorage.assert_called_once_with(api_version='storage.k8s.io/v1beta1', kind='StorageClass', metadata=meta, provisioner=provisioner)
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_createDeploymentFromFile(kubeConfig):
    """
    Do I create a Deployment kubernetes resource from a yaml manifest file?
    """
    pOpen = patch_open("data")
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'ExtensionsV1beta1Api',
        return_value=Mock(
            create_namespaced_deployment='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createDeploymentFromFile('/path')
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', body='data', namespace='default')


@pytest.inlineCallbacks
def test_createConfigMap(kubeConfig):
    """
    Do I create a configmap kubernetes resources in a namespace?
    """
    meta = 'happy'
    data = 'days'
    namespace = 'grn-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pPVC = patch.object(client, 'V1ConfigMap', return_value='thing')
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            create_namespaced_config_map='a',
        ),
        autospec=True,
    )
    with pApiMethod, pPVC, pCall as mCall:
        yield lib.createConfigMap(meta, data, namespace)
        mCall.assert_called_once_with('a', 'grn-se-com', 'thing')


@pytest.inlineCallbacks
def test_createService(kubeConfig):
    """
    Do I create a namespaced Service kubernetes resource from a yaml manifest file?
    """
    namespace = 'grn-se-com'
    fileData = 'data'
    pOpen = patch_open(fileData)
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            create_namespaced_service='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createService('/path', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', namespace, fileData)


@pytest.inlineCallbacks
def test_createServiceAccount(kubeConfig):
    """
    Do I create a Service Account kubernetes resource from a yaml manifest file?
    """
    namespace = 'grn-se-com'
    fileData = 'data'
    pOpen = patch_open(fileData)
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            create_namespaced_service_account='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createServiceAccount('/path', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', namespace, fileData)


@pytest.inlineCallbacks
def test_createClusterRole(kubeConfig):
    """
    Do I create a Cluster Role kubernetes resource from a yaml manifest file?
    """
    fileData = 'data'
    pOpen = patch_open(fileData)
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'RbacAuthorizationV1beta1Api',
        return_value=Mock(
            create_cluster_role='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createClusterRole('/path')
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', fileData)


@pytest.inlineCallbacks
def test_createClusterRoleBind(kubeConfig):
    """
    Do I create a Cluster Role Binding kubernetes resource from a yaml manifest file?
    """
    fileData = 'data'
    pOpen = patch_open(fileData)
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'RbacAuthorizationV1beta1Api',
        return_value=Mock(
            create_cluster_role_binding='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createClusterRoleBind('/path')
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', fileData)


@pytest.inlineCallbacks
def test_createIngress(kubeConfig):
    """
    Do I create a Ingress kubernetes resource from a yaml manifest file?
    """
    namespace = 'g-se-com'
    fileData = 'data'
    pOpen = patch_open(fileData)
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'ExtensionsV1beta1Api',
        return_value=Mock(
            create_namespaced_ingress='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createIngress('/path', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', namespace, fileData)


def test_createEnvVar(kubeConfig):
    """
    Do I create a environment variable kubernetes resource that references
    a value in a configmap?
    """
    actual = str(lib.createEnvVar('fun!', 'cmName', 'cmKey'))
    assert "'key': 'cmKey'" in actual
    assert "'name': 'cmName'" in actual
    assert "'name': 'fun!'" in actual
