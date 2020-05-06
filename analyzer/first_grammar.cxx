#encoding "utf8"

Main -> S;
PR -> "с" | "со";
Sbj -> Noun<gram="nom"> interp(SAO.Subject);
Sbj -> Noun<gram="nom"> interp(SAO.Subject) AnyWord<cut>* 'и'
	   Noun<gram="nom"> interp(SAO.Subject) AnyWord<cut>*;
Obj -> Noun<rt>;
S -> 	Noun<gram="nom", sp-agr[1]> interp(SAO.Subject) 'и'
		Noun<gram="nom", sp-agr[1]> interp(SAO.Subject)
		Word<kwtype=conn_verbs, rt, gram="V",sp-agr[1]>
		interp(SAO.Action)
		AnyWord<cut>* PR AnyWord<cut>* Obj<gram="ins">
		interp(SAO.Object);
S -> Sbj<sp-agr[1]>
	Word<kwtype=conn_verbs, rt, gram="V",sp-agr[1]>
	interp(SAO.Action)
	AnyWord<cut>* PR AnyWord<cut>* Obj<gram="ins">
	interp(SAO.Object);