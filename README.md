# 👩‍💻 프로젝트명 ( MRS )
- 사용자 정보 기반 영화 추천 서비스

<br>

## 📌 프로젝트 소개
- 다양한 분야와 기업에서 추천 시스템을 개발하고 도입하고 있다. 사용자가 좋아할 만한 콘텐츠를 추천 알고리즘은 어떻게 찾는지 학습하여 구현하고자 프로젝트를 진행하였다.
- 다양한 분야 중 '영화' 카테고리를 선정해 사용자 정보를 활용하여 영화 콘텐츠를 추천하고자 한다.

<br>

## 📎 서비스 목표
- 다양한 방법으로 영화를 추천 받을 수 있는 서비스를 제공하자.
- 기존 서비스에서 장점은 가져가고 아쉬운 점을 보완하자.

<br>

## 👨‍👧‍👧 팀원
- [정소희](https://github.com/HEEpage) : DB 모델링 및 설계, 사용자 관련 기능 구현, 사용자 API 정의, 웹페이지 구축
- [윤기연](https://github.com/kyeon06) : 데이터 수집 및 크롤링, DB 데이터 적재, 영화 API 정의, 웹페이지 구축
- [조하나](https://github.com/xnsl291) : 데이터 전처리 및 EDA, 콘텐츠 기반/협업 필터링 추천 모델링, 감상 포인트 기능 구현
- [김예림](https://github.com/yelimkin) : 데이터 전처리, 콘텐츠 기반/포스터 활용 추천 모델링, 영화 관련 기능 구현

<br>

## 📅 개발 기간
- 2022.12.29 - 2023.01.30

<br>

## ⚙️ 개발 환경
- Front-end : <img src="https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=Vue.js&logoColor=black"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">  <img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">

- Back-end : <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">

- ML/DL : <img src="https://img.shields.io/badge/sklearn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"> <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white">

- DB : <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 

- Deployment : <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white">

- IDE : <img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white"> 

- Communication Tools : <img src="https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white"> <img src="https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white">


<br>

## 👤 User Flow
<img src="https://user-images.githubusercontent.com/111492415/227709701-d5a7275e-cac4-4846-9d46-07dd82ac426e.png" style="width:800px">

<br>

## 💾 DB ERD
<img src="https://user-images.githubusercontent.com/111492415/227709742-c96982df-0b9f-438c-92cc-d977a86faff7.png" style="width:800px">

<br>

## 📽️ 구현한 서비스
### 1. 영화 추천 기능
- 사용자의 영화 기록을 기반으로 영화를 추천한다.
- 영화 기록이 적을 경우 장르 콘텐츠 기반 추천하고 영화 기록이 충분할 경우 협업 필터링 방식을 활용하여 추천한다.
- 사용자가 가장 재밌게 본 영화 포스터를 기반으로 비슷한 영화를 추천해준다.
- 감상포인트 기반 추천작도 확인할 수 있다.

<img src="https://user-images.githubusercontent.com/111492415/227708758-2781bbfa-c9e0-43a9-a85c-f25d976445da.png" style="width:400px"> <img src="https://user-images.githubusercontent.com/111492415/227708733-48cbbb53-aff8-4ada-b05b-22c2a3169f2f.png" style="width:370px"> 

### 2. 로그인/회원가입 기능
  - 신규 유저의 경우 선호장르 기반으로 영화를 추천한다. (회원가입시 선택)

<img src="https://user-images.githubusercontent.com/111492415/227709028-df941ca6-c839-4b3d-914d-6a6d9ac4c01b.png" style="width:370px"> 

### 3. 장르별 영화 목록 확인
  - 페이지네이션 적용, 최신순/평점순/제목순 필터링 가능

<img src="https://user-images.githubusercontent.com/111492415/227709155-5587c1d2-6463-4ed4-9d69-2d5964e516db.png" style="width:400px"> <img src="https://user-images.githubusercontent.com/111492415/227709255-bfc824d5-3700-415d-8de3-460e0358ae49.png" style="width:400px">

### 4. 영화 상세 페이지
  - 영화 평점을 남길 수 있다.
  - 관심 영화로 등록 or 취소할 수 있다.
  - 관람 가능한 OTT 서비스와 현재 어느 상영관에서 상영하는지 정보를 얻을 수 있다.

<img src="https://user-images.githubusercontent.com/111492415/227709872-fec38de7-fac4-48d6-9387-9fcff9a28677.png" style="width:700px">

### 5. 관심영화관리, 영화기록관리
  - 사용자의 관심영화와 평점을 남긴 영화에 대해 관리할 수 있다.
  
<img src="https://user-images.githubusercontent.com/111492415/227709590-968d1e3f-a315-467c-82b2-62bde17f8607.png" style="width:400px"> <img src="https://user-images.githubusercontent.com/111492415/227709543-bc566087-f009-45ae-bcd5-0f308fb1c044.png" style="width:390px">

### 6. 마이페이지
  - 기록 기반으로 사용자의 선호도를 확인할 수 있다.

<img src="https://user-images.githubusercontent.com/111492415/227709490-e6c64b62-1a21-4baa-8289-f34e46a758db.png" style="width:700px">

<br>

## 🤷‍♀️ 기대효과
1. 콘텐츠 선택의 간편화
- 다양한 영화 콘텐츠 중에서 사용자의 취향 분석을 통해 사용자가 자신의 취향에 따른 영화 콘텐츠를 간편하게 선택
2. 영화관 및 OTT 서비스 이용 증가
- 개인화된 추천으로 상영 영화 관람과 OTT 서비스 시청을 유도
3. 효율적인 판권 구매
- 부가 판권 시장에서 기업이 사용자들의 취향 분석을 통해 효율적인 판권 구매 가능

<br>

## ⭐ 개선사항
### [서비스 측면]
1. 사용자 기록 등록 유도를 위한 포인트 부여
- 영화 기록을 추가할 때마다 포인트를 부여하여 사용자의 서비스 사용을 유도하고자 함
2. 간편 가입 기능 추가
- 카카오나 네이버 API를 연동하여 간편하게 서비스에 가입할 수 있도록 함

<br>

### [추천 알고리즘 측면]
1. 사용자 기록이 많을 수록 추천 목록 생성 늦음
- 시간이 오래 걸리는 문제 개선 필요
