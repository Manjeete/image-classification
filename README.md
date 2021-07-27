# Image Classification using Tensorflow Inception v3
    Rest API for images classification

# STEP 1:
Register as user


```python
Register Endpoint (Only Post Request)

http://127.0.0.1:5000/register
```
```javascript
data : {
    
	"username":"<username>",
	"password":"<password>",
}

Response:{
    "msg":"You successfully signed up for this Api",
    "status":201
}

```

# STEP 1:
Send Image Url along with username and password.


```python
Register Endpoint (Only Post Request)

http://127.0.0.1:5000/classify
```
```javascript
data : {
    
	"username":"<username>",
	"password":"<password>",
    "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Plains_Zebra_Equus_quagga.jpg/1200px-Plains_Zebra_Equus_quagga.jpg"
}

Response:{
    "zebra":0.946465313436008,
    "hartebeest":0.0010960039217025042,
    "tiger, Panthera tigris":0.0009116057772189379,
    "ostrich,Struthio camelus":0.0006766317528672516,
    "prairie chicken,prairie grouse,prairie fowl":0.00060929298818744719
}

```
