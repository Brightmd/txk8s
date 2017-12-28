# txk8s.lib module


## **createPVC**
### Description:

Creates a persistant volume claim resource using the kubernetes python client.

See python-client docs for [CoreV1Api.create_namespaced_persistent_volume_claim](https://github.com/kubernetes-incubator/client-python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_persistent_volume_claim) for more details.

### Example 
```python
import txk8s

from twisted.internet import defer


def main()
    # create an instance of the twisted kubernetes client class
    txcli = txk8s.TxKubernetesClient()

    # create a kubernetes meta object
    meta = txcli.V1ObjectMeta(
        name='example-claim',
        annotations={
            'volume.beta.kubernetes.io/storage-class':  'example',
        },
    )

    # create a kubernetes spec object
    spec = txcli.V1PersistentVolumeClaimSpec(
        access_modes=['ReadWriteMany'],
        resources=txcli.V1ResourceRequirements(
            requests={
                'storage': '1Mi',
            },
        ),
    )

    # create PersistentVolumeClaim
    d = txcli.createPVC('res', meta, spec, namespace)
    d.addCallback(txcli.createPVC, meta, spec, namespace)

```

### Parameters
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**response** | **str** | The twisted deferred response when this function is executed as a callback | [required] 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata | [required]
**spec** | [**V1PersistentVolumeClaimSpec**](V1PersistentVolumeClaimSpec.md) | Spec defines the desired characteristics of a volume requested by a pod author. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims | [required]
**namespace** | **str** | The name of the namespace the PVC is created for.  Typically the value is the dashed hostname of the clinical partner. | [required] 


### Return type

Returns a Twisted deferred object.

See twisted documentation for details: [**twisted.internet.defer.Deferred**](https://twistedmatrix.com/documents/16.5.0/api/twisted.internet.defer.Deferred.html)