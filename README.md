# Django Samples

## Requirements

- Python >= 3.5
- Poetry >= 1.0

## Installation

```shell
poetry install
```



## Samples

### DRF Base64 ImageField

**[Test Code](https://github.com/LeeHanYeong/django-samples/blob/master/app/drf_base64/tests.py)**

- Image encode/decode test using python's base64 module  
    **drf_base64.tests.Base64ImageConvertTest**
- DRF API test to create a model instance with a FileField by sending a Base64 string  
    **drf_base64.tests.Base64ImageAPITest**

