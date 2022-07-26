
# Change Log
All notable changes to this project will be documented in this file.
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.


## [1.1.4] - 2022-07-19

 
### Added


### Changed
1. [ENUS] add color temperature(s) in dict/enUS/aliasF light(s) number one/two/three in dict/enUS/aliasD

### Need Fix


## [1.1.4] - 2022-07-18

 
### Added
1. V2server.py: a server to connect to devicetalk

### Changed
1. 中文程式TWnlp.py更新：已和英文版同步
2. error message: 更新為五種error message,詳情看[中文版錯誤訊息](https://github.com/gggaaammm/Voicetalk/blob/v2/User/dict/zhTW/errorlog_zhTW.txt)/[English ver. error message](https://github.com/gggaaammm/Voicetalk/blob/v2/User/dict/enUS/errorlog_enUS.txt)

### Need Fix
1. device talk template





## [1.1.3] - 2022-07-16

 
### Added

### Changed
1. param長度 = quantityV長度+stringV長度+key_id數量-keylist長度
2. keylist, key_id用於關鍵字轉數字(紅色=255, etc)
3. 中文版：數字問題, 暫時解決
4. 中文版：中文, 

### Need Fix
1. device talk
2. connect voicetalk to devicetalk
3. a param_dictionary check function if exist for type string
4. a unit dictionary to save unit(to use or to compare?)
5. 



## [1.1.2] - 2022-07-12

 
### Added
1. parameterTable增加
2. param_dict程式
3. 多dimension處理方式

### Changed
1. Database 修正, 預計刪除FeatureTable的value_dict
2. value_dict改為各個dimension各自處理. {'red': [255,0,0]} -> {'red':255}, {'red':0}, {'red':0}
3. quantityDetect儲存quantity 
4. token['V'] 改為不限一個


### Need Fix
1. need a devicetalk template
2. connect voicetalk to devicetalk
3. a param_dictionary check function if exist for type string
4. a unit dictionary to save unit(to use or to compare?)
5. 



## [1.1.2] - 2022-07-07
 

 
### Added
1. 錯字校正，詳見[中文校正列表](https://github.com/gggaaammm/Voicetalk/blob/v2/User/dict/zhTW/correction/correction.txt) 以及 [英文校正列表](https://github.com/gggaaammm/Voicetalk/blob/v2/User/dict/enUS/correction/correction.txt)

### Changed



### Need Fix
1. parameterTable
2. handleValue()
3. handleUnit()
4. checkminMax()
5. base unit 修正






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
7. error message #-5回傳修正
8. 三角燈亮度0 -> 0 not detected as number
9. 




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

 

 
