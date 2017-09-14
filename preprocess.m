function outSentence = preprocess(inSentence, language)
    
paranthesisMatch = regexp(inSentence,'(?<=\()[^(]+(?=\))','match');
prunedashes = regexprep(paranthesisMatch, '(-)', '$1 ');
sepdashes = regexprep(inSentence, paranthesisMatch, prunedashes);

if language == 'english'
    clitsplit = regexprep(sepdashes,'(n?''t|''[a-z]+)|([^\w\s])', ' $1');
else
    nole = regexprep(sepdashes,'(l'')(\w+)', '$1 $2');
    nomuet = regexprep(nole,'([cdjmnst]'')(\w+)', '$1 $2');
    noqu = regexprep(nomuet,'(qu'')(\w+)', '$1 $2');
    clitsplit = regexprep(noqu,'(puisqu'')(on)|(lorsqu'')(il)', '$1 $2');
end

mathsplit = regexprep(clitsplit,'([\+-\*/<>=])(\s?\d)', ' $1 $2');
various = regexprep(mathsplit,'(\w)([,:;\)"\?!\.])', '$1 $2');
startQuot = regexprep(various,'(["\(])(\w)', '$1 $2');
outSentence = startQuot;
end
