
# Change Log
All notable changes to this project will be documented in this file.
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.

## [1.1.2] - 2022-07-07
 

 
### Added
1. 多dimension的處理
2. quantityDetect(sentence)

### Changed
1. enspacy.py -> USnlp.py
2. zhspacy.py -> TWnlp.py
3. DevicefeatureTable.txt: add column 'dim'
4. token -> tokenlist in USnlp.py


### Need Fix
1. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) 「設定電扇風速到一。」 the sentence will be cause error of '1 '(with space inside the number) and handlevalue() is broken
2. USnlp.py修正
3. 修改DevicefeatureTable: 修改database
4. TWnlp.py修正
5. [ZHTW] 中文錯字修正
6. [ENUS] 英文錯字修正





## [1.1.2] - 2022-07-06
 

 
### Added
1. 多dimension的處理
2. quantityDetect(sentence)

### Changed
1. enspacy.py -> USnlp.py
2. zhspacy.py -> TWnlp.py
3. DevicefeatureTable.txt: add column 'dim'
4. token -> tokenlist in USnlp.py


### Need Fix
1. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) 「設定電扇風速到一。」 the sentence will be cause error of '1 '(with space inside the number) and handlevalue() is broken
2. USnlp.py修正
3. 修改DevicefeatureTable: 修改database
4. TWnlp.py修正
5. [ZHTW] 中文錯字修正
6. [ENUS] 英文錯字修正




## [1.1.1] - 2022-07-04
 

 
### Added
1. chinese number redirection to number: use num_zh.txt to help ckiptagger detect the number

### Changed
1. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) code remodulize as function
    1. tokenClassifier
    2. aliasRedirection
    3. tokenValidation


### Need Fix
1. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) 「設定電扇風速到一。」 the sentence will be cause error of '1 '(with space inside the number) and handlevalue() is broken
2. 二維的value該怎麼處理
3. 修改DevicefeatureTable: 修改database


## [1.1.1] - 2022-07-03




## [1.1.1] - 2022-07-04
 

 
### Added
1. chinese number redirection to number: use num_zh.txt to help ckiptagger detect the number

### Changed
1. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) code remodulize as function
    1. tokenClassifier
    2. aliasRedirection
    3. tokenValidation


### Need Fix
1. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) special case: "兩分鐘30秒" will ignore "30秒",  "兩分鐘"process successfully
2. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) 錯字校正: 風速到吧 -> 風速到8; 風速到時->風速到10
3. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) len(value_doc._.numerize()) > 1的狀況
4. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) value = value + Q_(int(quantitylist[q_id]), quantitylist[q_id+1]).to_base_units() 錯誤處理
5. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) Spell correction: number 'to'


## [1.1.1] - 2022-07-03

 
### Added
1. add the ckiptagger's module: POS and NER back for number and unit handling, it will increase the Data loading time from 4 sec to 25 sec


### Changed
1. [frontend](https://github.com/gggaaammm/Voicetalk/blob/v2/User/templates/index.html) startmessage and stopmessage 

### Need Fix
1. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) special case: "兩分鐘30秒" will ignore "30秒",  "兩分鐘"process successfully
2. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) 錯字校正: 風速到吧 -> 風速到8; 風速到時->風速到10
3. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) len(value_doc._.numerize()) > 1的狀況
4. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) value = value + Q_(int(quantitylist[q_id]), quantitylist[q_id+1]).to_base_units() 錯誤處理
5. [ENUS](https://github.com/gggaaammm/Voicetalk/blob/v2/User/enspacy.py) Spell correction: number 'to'



## [1.1.1] - 2022-07-01
 
 
### Added
1. chienese new unit conversion module


### Changed
1. remove chinese old unit conversion
2. all device will be pushed open when using other device feature

### Need Fix
1. chinese number undetected
2. spacy numerize in chinese not used

 
## [1.1.0] - 2022-06-29
  
Here we would have the update steps for 1.1.0 for people to follow.
 
### Added
1. add ckip word segmentation
 
### Changed
1. ckip now only use WS(word segmentation), POS and NER are removed to reduce loading time

 

 
