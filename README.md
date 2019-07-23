# Brunch Article Recommendation
```bash
$> tree -d
.
├── res
│   ├── contents
│   ├── predict
│   └── read
└── tmp
```
### 1. 추천 방법
- 평가 데이터와 제공 데이터의 겹치는 기간 (2.22~3.1)을 활용하여 이 기간동안 독자가 읽은 글과 비슷한 글을 추천

1. 2.22~3.1 기간 동안 각 독자가 특정 작가의 몇 개의 글을 읽었는지 확인 후 가장 많이 읽은 작가부터 불러옴
   독자가 읽은 특정 작가의 글 번호가 23 이라면, ex) @brunch_23, 그 글 번호 앞/뒤 +2개의 글 중 독자가 안 읽은 글이 있다면 추천

2. 1번 방법으로 추천 글이 100개가 채워지지 않을 경우, 독자가 following 하고 있는 작가가 있다면, 
그 작가의 글 중 2.22~3.1 기간동안 가장 많이 조회된 글 순서대로 불러와 그 중 독자가 읽지 않은 글을 추천 (각 작가 당 15개 글) 

### 2. 실행방법
- predict/dev.users에 대한 추천 결과를 생성
```
$> python recomendation_final.py recommend ./res/predict/dev.users recommend.txt
```

- predict/test.users에 대한 추천 결과를 생성
```
$> python recomendation_final.py recommend ./res/predict/test.users recommend.txt
```
