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
  
