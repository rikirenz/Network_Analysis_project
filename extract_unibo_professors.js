/**
 * Created by Riccardo Candido on 26.11.16.
 *
 * This script was executed at the following url address:
 * http://www.informatica.unibo.it/it/Dipartimento/docenti-e-ricercatori?pagenumber=1&pagesize=1000&sort_on=getObjPositionInParent&searchtext=
 * on 26.11.16 with the following browser: Google Chrome Version 54.0.2840.98 (64-bit)
 *
 *
 * This script exports the "docenti ricercatori" list from the UNIBO site for the CS department
 */

var authors = [];
a=$('.fn.name');
for (var index = 0; index < a.length; ++index) {
    authors.push('"' + a[index].innerHTML + '"');
}
console.log('{ "authors": [' + authors + '] }');
