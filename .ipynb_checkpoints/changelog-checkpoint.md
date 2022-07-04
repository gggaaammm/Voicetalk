
# Change Log
All notable changes to this project will be documented in this file.

## [Unreleased] - 2022-07-XX
 
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.
 
### Added

### Changed
 
### Fixed



## [1.1.2] - 2022-07-03
 
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.
 
### Added
1. add the ckiptagger's module: POS and NER back for number and unit handling, it will increase the Data loading time from 4 sec to 25 sec
2. chinese number redirection to number: use num_zh.txt

### Changed
1. [frontend](https://github.com/gggaaammm/Voicetalk/blob/v2/User/templates/index.html) startmessage and stopmessage 

### Need Fix
1. [ZHTW](https://github.com/gggaaammm/Voicetalk/blob/v2/User/zhspacy.py) special case: "兩分鐘30秒" will ignore "30秒", but "兩分鐘"process successfully
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

 

 
