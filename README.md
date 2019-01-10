# ll1parser
## Features：
1. 计算文法的First集，Follow集，预测分析表<br>
2. 分析输入串是不是指定文法的句子  
## 演示:    
1. 输入文法为  
E->TK  
K->+TK|@  
T->FM  
M->*FM|@  
F->i|(E)  
2. 输入文法为  
E->TK  
K->+TK|@  
T->FM  
M->*FM|@  
F->i|(E)  
**F->[E]**  
3. 输入文法为  
E->TK  
K->+TK|@  
T->FM  
M->*FM|@  
F->i|(E)  
**F->[E]**  
**F->[F]**  
