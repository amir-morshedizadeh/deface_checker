# deface_checker

A tool for checking integrity of the site in order to monitor any defacement or unauthorized changes in the main or landing page of your sites.

## How it works?

* It sends a request to the URL then saves the response in “page.txt”
*	After reaching to the end of URLs in “urls.txt”, it would send a request again and saves the response in the memory.
*	Both responses are compared using “diff-match-patch” library created by Google.
*	If any changes like adding or removing tags, strings and …, are detected between these responses, it makes an HTML file with added and removed parts with highlighted colors.
*	The code sends the generated HTML file via a Telegram Bot (or Bale Bot) to a Telegram group.
*	Admins are joined to the group and could check the HTML file for any changes within the site.

## Steps to run

*	Create a “urls.txt” file within the “c:\output2” or change the folder within the code.
*	Create a Telegram bot and a Telegram group and add the information to the source code.
*	Run the code

## How to tune?

For every site there could be a "whitelist_.txt" file inside the created folder for each site.
It is used for minimizing false positives before sending pages to compare.
For example, response of a server may contain a VIEWSTATE value for every response, so we need to remove VIEWSTATE value before comparing for a more reliable result.
Any html tag or content could be added to this file to improve the result.


## There are 4 different types of defining exceptions in the "whitelist_.txt" file:



### 1 - Removing value of an attribute:
---
#### Response example:
*<input id="__VIEWSTATE" name="__VIEWSTATE" type="hidden"  value="31DgVHUW6lLKGiKNEH93"/>*

#### Rule format defined in “urls.txt”:
*tag_name,attribute_name:attribute_value*

#### Exception example:
*input,id:__VIEWSTAT*

#### Output:
*Input tag containing “id= __VIEWSTATE” is removed from the response before compare.*




### 2 - Removing value of a tag via regex:
---
#### Response example:
*<img src="WebResource.axd?id=11111">*

#### Rule format defined in “urls.txt”:

*tag_name,attribute_name:attribute_value,regex*

#### Exception example:

*img,src:WebResource.axd,regex*

#### Output:
*IMG tag containing “src= WebResource.axd?id=11111” is removed from the response before compare.*




### 3 - Removing strings and var between tags:
---
#### Response example:
*<script type="text/javascript"> var sd_persiandatepicker_MAXDATE = new Date(2022,5,9); </script>*

#### Rule format defined in “urls.txt”:
*tag_name,:string,regexstring*

#### Exception example:
*tag_name,:var sd_persiandatepicker_MAXDATE .*?\);,regexstring*

*SCRIPT tag containing “sd_persiandatepicker_MAXDATE” string is removed from the response before compare.*




### 4 - Removing values from some attributes that can not be used with Rule #1:
---
#### Response example:
*<img alt="SMALL" src="https://example.com/pic.jpg" class=”in-press press-wired”>*

#### Rule format to define in “urls.txt”:
*ag_name,attribute_name:attribute_value string*

#### Exception example defined in “urls.txt:
*div,class:in-press press-wired*

#### Output:
*IMG tag containing “class= in-press press-wired” is removed from the response before compare.*



Note
True Negative
