# deface_checker

A tool for checking the integrity of your sites(the main or landing page of your site) in order to monitor for any possible defacement or unauthorized changes in the code.

## How it works?

* It sends a request to the url then saves the response in “page.txt” file.
*	After reaching to the end of urls in “urls.txt”, it sends a request again then saves the response in the memory.
*	Both responses are compared using “diff-match-patch” library created by Google.
*	If any changes like adding or removing tags, strings and whatever are detected between these responses, it then makes an HTML file with added and removed parts with highlighted colors.
*	It sends the generated HTML file via a Telegram Bot (or Bale Bot) to a Telegram/Bale group for SOC team to analyze the event.

## Steps to run

*	Create and name a file as “urls.txt” to cover all your assets then put the file in the “base_dir” variable in the code.
*	Create a Telegram bot and group then add them to the source code:
###### Telegram:  [Telegram Bot](https://core.telegram.org/bots#how-do-i-create-a-bot)
###### Bale:  [Bale Bot](https://dev.bale.ai/quick-start)
*	Run the code and analyse receiving events. If required try to tune the recieving alert.

## Why and how to tune?

Consider a web server's response that contains a VIEWSTATE value in every response. So we need to remove the VIEWSTATE value to provide more reliable alerts for security analysts.
For every site there could be a "whitelist_.txt" file inside the created directory for each site.
It is used for minimizing false positive alerts by defining some exceptions in the "whitelist_.txt".

Any html tag or content could be added to this file.


## There are 4 different types of defining exceptions in the "whitelist_.txt" file:



### 1 - Removing value of an attribute:
---
#### Response example:
*&lt;input id="__VIEWSTATE" name="__VIEWSTATE" type="hidden"  value="31DgVHUW6lLKGiKNEH93"&gt;*

#### Rule format defined in “urls.txt”:
*tag_name,attribute_name:attribute_value*

#### Exception example:
*input,id:__VIEWSTAT*

#### Output:
*Input tag containing “id= __VIEWSTATE” is removed from the response before compare.*




### 2 - Removing value of a tag via regex:
---
#### Response example:
*&lt;img src="WebResource.axd?id=11111"&gt;*

#### Rule format defined in “urls.txt”:

*tag_name,attribute_name:attribute_value,regex*

#### Exception example:

*img,src:WebResource.axd,regex*

#### Output:
*IMG tag containing “src= WebResource.axd?id=11111” is removed from the response before compare.*




### 3 - Removing strings and var between tags:
---
#### Response example:
*&lt;script type="text/javascript"> var sd_persiandatepicker_MAXDATE = new Date(2022,5,9); &lt;/script>*

#### Rule format defined in “urls.txt”:
*tag_name,:string,regexstring*

#### Exception example:
*tag_name,:var sd_persiandatepicker_MAXDATE .*?\);,regexstring*

*SCRIPT tag containing “sd_persiandatepicker_MAXDATE” string is removed from the response before compare.*




### 4 - Removing values from some attributes that can not be used with Rule #1:
---
#### Response example:
*&lt;img alt="SMALL" src="https://example.com/pic.jpg" class=”in-press press-wired”&gt;*

#### Rule format to define in “urls.txt”:
*ag_name,attribute_name:attribute_value string*

#### Exception example defined in “urls.txt:
*div,class:in-press press-wired*

#### Output:
*IMG tag containing “class= in-press press-wired” is removed from the response before compare.*



> __I love poll request.__
