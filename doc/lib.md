# txk8s.lib module


## **createPVC**
### Description:

Creates a persistant volume claim resource using the kubernetes python client.

See python-client docs for [CoreV1Api.create_namespaced_persistent_volume_claim](https://github.com/kubernetes-incubator/client-python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_persistent_volume_claim) for more details.

### Example 
```python
import txk8s


# create an instance of the twisted kubernetes client class
txcli = txk8s.TxKubernetesClient()

# create a kubernetes meta object
meta = txcli.V1ObjectMeta()

# create a kubernetes pvc spec object
spec = txcli.V1PersistentVolumeClaimSpec()

namespace = 'example-ns'

# create the PersistentVolumeClaim
# returns a twisted deferred
d = txcli.createPVC(meta, spec, namespace)
```

### Parameters
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata | [required]
**spec** | [**V1PersistentVolumeClaimSpec**](V1PersistentVolumeClaimSpec.md) | Spec defines the desired characteristics of a volume requested by a pod author. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims | [required]
**namespace** | **str** | The name of the namespace the PVC is created for. | [required] 


### Return type

Returns a Twisted deferred object.

See twisted documentation for details: [**twisted.internet.defer.Deferred**](https://twistedmatrix.com/documents/16.5.0/api/twisted.internet.defer.Deferred.html)


## **createStorageClass**
### Description:

Creates a storageClass resource using the kubernetes python client.

See python-client docs for [StorageV1beta1Api.create_storage_class](https://github.com/kubernetes-incubator/client-python/blob/master/kubernetes/docs/StorageV1beta1Api.md#create_storage_class) for more details.

See Kubernetes docs for [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner) for details.

### Example 
```python
import txk8s

from twisted.internet import defer


def main()
    # create an instance of the twisted kubernetes client class
    txcli = txk8s.TxKubernetesClient()

    # a provisioner that determines what volume plugin is used
    provisioner = 'aws-efs'

    # create a kubernetes meta object
    meta = txk8s.V1ObjectMeta()

    # create the storageClass
    # returns a twisted deferred
    d = txcli.createStorageClass(meta, provisioner)
    return d
```

### Parameters
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata | [required]
**provisioner** | **str** | A provisioner that determines what volume plugin is used | [required]


### Return type

Returns a Twisted deferred object.

See twisted documentation for details: [**twisted.internet.defer.Deferred**](https://twistedmatrix.com/documents/16.5.0/api/twisted.internet.defer.Deferred.html)