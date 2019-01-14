

# Application Management: Running, Stopping, Scaling, Deleting

## Delete
```
kubectl delete pods <pod> 
```
### Force Delete
```
kubectl delete pods <pod> --grace-period=0 --force
```