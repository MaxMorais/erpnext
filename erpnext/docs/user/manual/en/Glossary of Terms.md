# this is a stubb of a to be build "Glossary of Terms" for ERPNext

The intention is to build a Glossary of terms (i.e. 'Site', 'Form', etc.) and what they exactly mean in the logic of ERPNext
Initial goal is to help me understanding ERPNext and I will populate it as I go along discovering. Hopefully at some point others might add Definitions or correct/clarify this existing Glossary, and this might turn out to be useful for others as well

It is to be decided at what point it will be serious, big, good enough to do a PR to the orgiginal erpnext repository

===================================================

**Glossary of Terms**

**Site** - [add definition here]

**Like** (in Filter to filter list items) - same meaning as "Contains" (i.e Filter term 'SIN' will find Sales Invoices (SINV). "Like" has no ability to find misstyped terms though. It will not find 'tasks', when searching for 'taks'. 'Like' is not case sensitive

**Equals** (in Filter to filter list items) - will Filter the exact term which is put in. (i.e. Filter term 'SINV-0001' will find one specific Sales Invoice (SINV-0001). Neither 'SINV' nor 'SIN*' will find any Sales Invoice (SINV-xxxxx). 'Equals' is not case sensitive

**Filter** - is a condition or rule to limit the result of a query, a link field, etc.
