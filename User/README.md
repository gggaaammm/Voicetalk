# Voicetalk User guide


## Requirement

1. Domain name
2. SSL Authentication

For applying domain name, please contact your organization administrator
For applying SSL auth, check out [certbot official](https://certbot.eff.org/)


## 1. Setup ckiptagger(zh-TW)

```
pip install -U ckiptagger[tf,gdown]
```
CkipTagger is a Python library hosted on PyPI. Requirements:

python>=3.6
tensorflow>=1.13.1 / tensorflow-gpu>=1.13.1 (one of them)
gdown (optional, for downloading model files from google drive)
(Minimum installation) If you have set up tensorflow, and would like to download model files by yourself.

`pip install -U ckiptagger`

(Complete installation) If you have just set up a clean virtual environment, and want everything, including GPU support.

`pip install -U ckiptagger[tfgpu,gdown]`

for more information, visit [ckiptagger official github](https://github.com/ckiplab/ckiptagger)

## 2. Setup enspaCy (en-US)

1. install spaCy
```
pip install -U spacy
```

2. download english model

```
python -m spacy download en_core_web_sm
```

for more information, visit [enspaCy official site](https://spacy.io/usage)


## 3. Setup server


```
python3 server.py
```