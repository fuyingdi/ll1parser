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
![IMAGE](https://github.com/fuyingdi/ll1parser/blob/master/Snipaste_2019-01-10_20-21-43.png)   
![IMAGE](https://github.com/fuyingdi/ll1parser/blob/master/Snipaste_2019-01-10_20-24-13.png)  
![IMAGE](https://github.com/fuyingdi/ll1parser/blob/master/Snipaste_2019-01-10_20-24-54.png)
![IMAGE](https://github.com/fuyingdi/ll1parser/blob/master/Snipaste_2019-01-10_20-25-21.png)
2. 输入文法为  
E->TK  
K->+TK|@  
T->FM  
M->*FM|@  
F->i|(E)  
**F->[E]**  
![IMAGE](https://github.com/fuyingdi/ll1parser/blob/master/Snipaste_2019-01-10_20-28-57.png)
![IMAGE](https://github.com/fuyingdi/ll1parser/blob/master/Snipaste_2019-01-10_20-28-49.png)
3. 输入文法为  
E->TK  
K->+TK|@  
T->FM  
M->*FM|@  
F->i|(E)  
**F->[E]**  
**F->[F]**  
![IMAGE](https://github.com/fuyingdi/ll1parser/blob/master/Snipaste_2019-01-10_20-29-31.png)
