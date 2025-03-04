# bitamin_winter_proj
BITAmin 12th &amp; 13th Joint Mini Project - Netflix stock close price prediction with news topic and sentiment 📊

# Version
- Python version : 3.9~3.11
- PyTorch version : 2.1.0+cu121
- scikit-learn version : 1.3.2
- Matplotlib version : 3.7.2
- selenium version : 4.17.2~ 

# 프로젝트 개요
### 배경
- 입력 시퀀스의 길이를 늘리는 것이 주가 예측에 효과적일까?
- 뉴스 토픽 모델링/감성 분석을 통한 인기 주식 예측은 기존에 많았는데 주가 예측에도 효과적일까?

### 주요 내용
- 장기적인 추세 반영에 효과적인 모델 판별 : LSTM vs GRU vs Transformer
- 실험을 통한 파라미터 튜닝
- 뉴스 데이터의 영향력 판단

# 주요 전처리
### 타겟
- Close vs 1d_RoC(Range of Change) : 예측 타겟 컬럼을 '종가'와 '1일 변화량'으로 비교하여 성능 실험
- TA Library로 보조지표 추가
- Peer analysis : 주가 동향이 유사한 핀터레스트, 메타플랫폼스, 스포티파이 주가를 반영
- 뉴스 토픽, 감성 : moving average, moving mode 값으로 반영 → 주식 보조지표인 이동평균선과 같은 개념으로 뉴스도 추세를 갖고 있을 것이라 가정

# 실험 결과에 대한 통계 검정
### t-test
![t-test](https://github.com/skier-song9/bitamin_winter_proj/blob/master/ppt/imgs/ttest.png) 
- 모든 모델에서 t-test의 p-value가 0.05 이상이므로 귀무가설인 “데이터셋은 RMSE에 영향을 주지 않는다“를 기각할 수 없다.
∴ 본 실험에서는 뉴스 감성분석, 토픽 데이터가 주가 예측에 효과적이라고 하기 어렵다.

### ANOVA 
GRU 모델의 실험 결과는 정규성을 만족하지 않으므로 ANOVA 분석을 수행할 수 없다.
![anova](https://github.com/skier-song9/bitamin_winter_proj/blob/master/ppt/imgs/anova.png)
- LSTM과 Transformer 모델의 데이터에서의 p-value가 0.05 이하이므로 귀무가설인 “입력 시퀀스의 길이가 달라도 RMSE에는 차이가 없다.“를 기각할 수 있다.
∴ 입력 시퀀스 길이에 따라 RMSE가 달라질 수 있다.

### TurkeyHSD 사후검정 
ANOVA 검정의 결과로 나타난 입력 시퀀스 길이 간의 차이가 어떤 그룹들 사이에서 유의미한지 확인한다.
![turkeyHSD](https://github.com/skier-song9/bitamin_winter_proj/blob/master/ppt/imgs/turkeyHSD.png)
1. LSTM의 경우 30과 60, 30과 120 그룹 간의 차이가 유의미하다고 나타났다. Seq_Length가 30일 때 최적의 RMSE값을 가지므로 이로 미루어 보아 장기적인 추세 반영이 효과적이라고 볼 수 없다.
2. Transformer도 마찬가지로 30과 60 그룹 간의 차이만 유의미하고 30일 때 RMSE값이 제일 작으므로 장기적인 추세 반영의 효과성에 대해서는 회의적이다.

# 최종 결과
### 최적의 파라미터 조합
![best param set](https://github.com/skier-song9/bitamin_winter_proj/blob/master/ppt/imgs/best_param.png)

### 모델별 예측 결과
![LSTM](https://github.com/skier-song9/bitamin_winter_proj/blob/master/ppt/imgs/result_lstm.png)
![GRU](https://github.com/skier-song9/bitamin_winter_proj/blob/master/ppt/imgs/result_gru.png)
![Transformer](https://github.com/skier-song9/bitamin_winter_proj/blob/master/ppt/imgs/result_transformer.png)
