#include <iostream>
#include <string.h>
using namespace std;
int tokenClassifier(string word);

int main()
{   
    int i,j,V=0, v=0;                                 // j is counter of word set, i is category of token
    string A="", D="", F="", u="";                    // A/D/F/V is token, v=number of V, u=unit of V
    int token[4] = {0};                               // token[] is a counter of tokenset

    
    
    // Voicetalk frontend
    // input: User select language by clicking on select 
    // webpage GUI: languagelist, recordbutton, recognition result, system response
    
    languageList = ["en-US","zh-TW"]
        
    //webpage default value
    language = "zh-TW"             // set zh-TW as default language
    micbutton.state = "start";     // ["start", "end"], set start as default state
    recognitionResult = "";
    systemResponse = ""
   
    
        
    //GUI    
    if(languageList.onchange()){
        language = selectLanguage(languageList) // step 1: user select certain language
        micbutton.state = "end"
        recognitionResult = ""
        systemResponse = ""    
    }
    
    //WebSpeechAPI
    var recognition = new webkitSpeechRecognition(); //  new a voice recognition object(Web speech API)
    recognition.lang = language;                     //  set recognition object language
    
    
    if(micbutton.onclick()){
        if(micbutton.state == "start"){                  // step 2: user press start button
            recognition.onstart()
            }
        if(micbutton.state == "end"){
            recognitionResult = recognition.onresult()    // user press stop button, system stop manually
        }
    }
    else if(recorgnition.onend()){
        recognitionResult = recognition.onresult()    // no more mic input, system stop automatically
                                                      // step 3: Web speech API get recognition result
    }
           
    
    
    // Voicetalk backend
    // Tokenize subsystem.Tokenize tool
    string wordset[] = parsingSentence(recognitionResult, language); // step 4: tools tokenize sentence to set of words by language
                                                                     // Tokenize tools: ckiptagger(zh-TW), spaCy(en-US)
    
                                            
    while(j< wordset.size())                  // stpe 5: for each loop, select 1 word
    { 
        i = tokenClassifier(wordset[j]);      // stpe 6: classify word to token
        
        switch(i){
            case 0:
                A = wordset[j];
            case 1:
                D = wordset[j];
            case 2:
                F = wordset[j];
            case 3:                           // step 7: if token classified as V, do unit converion if need V
                while(tokenClassifier(wordset[j] == 3)){  
                    if(check_number(wordset[j]) == false){// no number in word set, 
                        V = wrodset[j];                   // V is type string and break the loop. ex: [set, light, color, to, 'red']
                        break;
                    }
                    else{
                        v = float(wordset[j]);             // save word as v(number)
                        j = j+1;                           // select next word
                        
                        
                        if(check_unit(wordset[j]) == false){
                            V = v;                        // next word is not unit. ex: [Set, light, brightness, to, 8]
                            break;                        // use default value v and break the loop
                        }
                        else if(check_unit(wordset[j]) == true){ // if next word is unit ex: [Set, timer, 3, minutes]
                            u = wordset[j]                 // save word as u(unit)
                            V = V+unitConversion(v,u)      // add unit conversion result to V. ex: unitConversion(3, minutes) = 180 secs
                                
                            if(check_number(wordset[j+1]) == false){
                                break;                     // if next loop is no longer number, break the loop. ex: [3, minutes, in, timer]
                            }
                            else j = j+1;                  // go to next loop, ex:[3,minutes,'10',seconds]
                        }
                    }
                }
        }
                
        token[i] = token[i]+1;                   // step 7: token[i] counter++, iterate next loop
        j = j+1;    
                       
        if(token[i]> 1)                         // step 8: if token[i] exceed 1 time
            return error
    }
    
    if( (A=="" && D=="") || (F==""))        // step 9: if A/D not exist or F not exist, return error
    {
        return error
    }
    
    //Parsing subsystem
    if(supportLookup(A,D,F,V) == true) continue;     // step 10: check if A/D(device) has such F(device feature)
    else return error
    
    if(ruleCheck(F) == 2) continue;            // step 11: check if device feature F(token[2]) is rule1 / rule2
    else return rule1_success
    
    if(valueCheck(F,V) ==  true) return rule2 success      // step 12: check if F(device feature) support V(device feature value)
    else return error
        
    //SA    
    if(rule1_success||rule2_success)                      // step 13: Send Device(s), IDF, value via Devicetalk
        sendIoT(A,D,F,V)
        
        
    // Voicetalk frontend: system response                 // step 14: response output to frontend's GUI
    if(error == true){
        systemResponse = (language = "zh-TW")? "聽不懂，請重講" : "I'm sorry, try again."
    }
    else{
        systemResponse = (language = "zh-TW")? "收到，" : "OK, "
        systemResponse.append(A,D,F,V)
    }

}

int tokenClassifier(string word)
{
    if(word is in dictionary A) return 0;
    else if(word is in dictionary D) return 1;
    else if(word is in dictionary F) return 2;
    else if(word is in dictionary V or check_number(word) == true) return 3;
    else return -1;
}