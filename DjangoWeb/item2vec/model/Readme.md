# Item2Vec를 만들기
유저 테이블에 있는 prdcd_seq 컬럼을 가져온다. 값들은 아이템 테이블에 있음. 
시퀀스 데이터 덩어리 ( "item, item, item" -> [item, item, item])을 바꿈
Skip-Gram 데이터를 만들자.  (input, input label input input )


## Skip-Gram에 대해서
CBOW의 반대 개념, 중앙의 단어를 통해 주변 단어를 예측

## Positive Sampling
윈도우 사이즈 미만의 데이터는 필터링    
필터링 된 데이터로 중앙 단어(Target)를 통해 주변 단어(Context) Pair를 생성한다.
(Target, Left_Context_Elem_1), (Target, Left_Context_Elem_2), ..., (Target, Right_Context_Elem_1) ...    
 

## Negative Sampling
사용자가 지정한 Window Size에 없는 데이터를 뽑는다.
Positive Pair 들 중에 안나온 Pair를 찾아보자.
저기에서 나온 Items.csv에 파악되는 아이템의 수는 총 3643인데 그렇다면
3643 * 3643 ( 13271449 elems, 천만이네...? ) 테이블을 만들어서 카운팅 테이블을 만들어 봐야 하남?
Row의 Index는 Target의 Index, Column의 Index는 Context의 Index를 가진다.
어쩌다 보니 그 Positive Pair에 등장하지 않는 Pair도 만들었네 ... 뭐 별 의미는 업는 듯
Posititive Pair중 하나가 들어오면 Negative Pair를 만들 Context를 생성하는데 
그럴려면 key - prdcd, value - set(prdcd)

## Sub-Sampling


# items.csv 겹치네...
150510000002,필보이드,15051,바디,샤워오일 대즐링 피버 [50ml/200ml],13000,2717
150510000002,필보이드,15051,바디,샤워오일 대즐링 피버 [50ml/200ml],50000,1272

이거 겹치는거 어쩌지 ... 지금은 어쩔 수가 없으니 ... items_dict 만들떄 봐야지 아니지 
pair occurence table 만들떄 그냥 max(dict.values)로 커버 해야지

## 아... 
item Fever
인리치드 시드 바디오일

## API 추가, SWAGGER UI에서 테스트 가능 
## URL = http://10.160.210.118:8080/swagger/