bing_search_for_stata
=====================

Stata program for conducting Bing search on variable values.

Some uses for this program include:
- Matching (e.g. multiple datasets with movie or song titles)
- Disentangling names (e.g. "John Smith CEO" and "John Smith")

The eventual syntax for the Stata command will be:

<code> bingsearch varlist [if] [in], URLvar(urlvarname) APIkey(apikeystring) [Site(sitestring) TITLEvar(titlevarname) EXACTphrase] </code>

# Description
For each observation where the value of urlvarname is missing, the *bingsearch* command will concatenate values from varlist and conduct a search on Bing providing the URL of the first result in variable urlvarname, and optionally the title of the first result in variable titlevarname.

# Options
URLvar(urlvarname) specifies the variable name that will store the URL value from the first result. If urlvarname does not exist it will be generated. If it does exist, then the search will only execute for observations where urlvarname is missing.

APIkey(apikeystring) specifies the Bing API key.

Site(sitestring) specifies a site domain if the user wants to narrow the search to a specific website (i.e. the search includes the string, "site:sitestring")

TITLEvar(titlevarname) specifies the variable name that will store the title value from the first result. If this option is not specified the title will not be stored. If it is specified and no variable exists, one will be created. If the variable exists any existing values will be overwritten.

EXACTphrase specifies whether the search string should be searched as an exact phrase (i.e. the stirng will be included in quotes).


# Remarks
The function requires the user to create an API key on Microsoft's Azure marketplace at https://datamarket.azure.com. Additionally, depending on the number of queries (i.e. number of observations), the user of this function may be requird to subscribe to a monthly access subscription. A summary of pricing can be found here:
https://datamarket.azure.com/dataset/bing/searchweb
WARNING! If you do not plan on using this function on an ongoing basis, be sure to change your subscription to the free option when you have completed your search.

The variable urlvarname can be an existing variable. If it exists, the function only conducts the Bing search for observations where there is no value in varname (this is to allow for you to return to the search, in the event the bing API breaks down or the search fails). If urlvarname does not already exist, then the function will create the variable.

The variable titlevarname can also be existing variable. If it exists, *any existing variables will be overwritten* for any observations where a search is conducted (i.e. urlvarname is missing) and there is an existing value in titlevarname.

The Python file contains the current implementation in python of the command importing a .csv file and then searching imdb.com.

The planned execution for the Stata command:

1. Check variable existence.
    1.1. Check if urlvarname exists. If it does not, then create it.
    1.2. Check if titlevarname exists. If it does not, then create it.
2. Create a temporary variable, queryvar, that is a concatenation of the string values in varlist separated by a space.
    2.1. Clean the values to make them searchable strings (below is everything I know that needs to be done)
        replace `queryvar' = itrim(trim(`queryvar'))
        replace `queryvar' = subinstr(`queryvar', "%",   "%25", .)
        replace `queryvar' = subinstr(`queryvar', " ",   "+",   .)
        replace `queryvar' = subinstr(`queryvar',`"""',  "%22", .)
        replace `queryvar' = subinstr(`queryvar', `"'"', "%27", .)
        replace `queryvar' = subinstr(`queryvar', "#",   "%23", .)
        replace `queryvar' = subinstr(`queryvar', "$",   "%24", .)
        replace `queryvar' = subinstr(`queryvar', "&",   "%26", .)
        replace `queryvar' = subinstr(`queryvar', "+",   "%2B", .)
        replace `queryvar' = subinstr(`queryvar', "!",   "%21", .)
        replace `queryvar' = subinstr(`queryvar', "(",   "%28", .)
        replace `queryvar' = subinstr(`queryvar', ")",   "%29", .)
        replace `queryvar' = subinstr(`queryvar', ":",   "%3A", .)
    2.2. If EXACTphrase is specified, affix open and closing quotes (" or %22?) around the value.
    2.3. If Site is specified, then affix the string to the end of the value, separated by a '+' (and outside the quotes created in 2.2 if EXACTphrase was specified)
3. For each observations
    3.1. If varname has a value or queryvar is missing for the observation, then go on to the next observation
    3.2. Search bing for the value in queryvar and return the URL from the first result to the value for urlvarname (and the title in titlevarname if specified)