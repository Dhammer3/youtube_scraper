def convert_text_to_num(subs):
        subs=subs.text
        sum=""
        i=0
        char=subs[0]
        while(char!="K"):
            if(char!='.' or char!="K"):
                sum+=subs[i]
            i+=1
            char= subs[i]

        if(char=="K"):
            return int(sum)*1000
        if(char=="M"):
            return int(sum)*1000000
        return int(sum)