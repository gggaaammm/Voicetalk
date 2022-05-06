# Voicetalk User guide

## Before start

### 1. download ckiptagger data

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

###
