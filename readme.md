# payhere - 가계부

## 📚 Skills
<br>

 - Language

    ![python](https://img.shields.io/badge/python-3.9-3670A0?logo=python&logoColor=white)

 - FrameWork

    ![Django](https://img.shields.io/badge/django-3.2.13-%23092E20?&logo=Django&logoColor=white)
    ![DjangoRest](https://img.shields.io/badge/DJANGOREST-3.13.1-ff1709?logo=django&logoColor=white&color=ff1709&labelColor=gray)
    
 - DataBase 

    ![MySQL](https://img.shields.io/badge/mysql-5.7-0073ca.svg?logo=mysql&logoColor=white)

 - Deploy 

    ![AWS](https://img.shields.io/badge/AWSE3-%23FF9900.svg?logo=amazon-aws&logoColor=white)
    ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
    ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?logo=nginx&logoColor=white)
    ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?logo=gunicorn&logoColor=white)

 - ETC

    ![GitHub](https://img.shields.io/badge/github-%23121011.svg?logo=github&logoColor=white)
    ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?logo=swagger&logoColor=white)<br><br>

## ✅ 프로젝트 소개
<br>

  - 가계부 생성이 가능하여 목적에 따라 수입,지출 관리가 가능
  - 삭제 된 데이터들은 언제든지 복구가 가능<br>
<br>

## 📌 요구 사항
<br>

  - 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다.

  - 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다.

  - 로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.

  - 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다.

    - 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
    - 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
    - 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
    - 삭제한 내역은 언제든지 다시 복구 할 수 있어야 한다.
    - 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다.
    - 가계부에서 상세한 세부 내역을 볼 수 있습니다.  
<br>

## 🔑 기능구현 목표
<br>

- 회원가입 구현

- 로그인, 로그아웃 구현
- 가계부 Create(POST) 구현
- 가계부 Read(GET) 구현
- 가계부 Update(PATCH) 구현
- 가계부 Delete 구현(Delete/Delete_Flag)
- 가계부 List 기능 구현(사용중인 가계부/삭제된 가계부)
- 가계부 Detail 기능 구현
- 사용자 권한 처리 구현(JWT를 활용한 Permission 설정)
- JWT(DRF-SimpleJwt) 활용
- 배포(AWS & Docker(Nginx+gunicorn+MySQL))
- Swagger를 활용한 API 기능 문서화<br><br>


## 📁API Doc
<br>

|Action| Method| URL|
|-----|----|----|
|회원가입| POST| users/signup
|로그인| POST| users/signin
|로그아웃| POST| users/signout
|가계부 작성| POST| account-books
|가계부 리스트| GET| account-books
|가계부 삭제 리스트| GET| account-books/deleted_list
|가계부 수정| PATCH| account-books<int: book_id>
|가계부 삭제,취소| PATCH| account-books<int: book_id>
|가계부 내역 작성| POST| account-books/<int: book_id>/accounts
|가계부 내역 리스트| GET| account-books/<int: book_id>/accounts
|가계부 내역 삭제 리스트| GET| account-books/<int: book_id>/accounts/deleted_list
|가계부 내역 상세조회| GET| account-books/<int: book_id>/accounts/<int: accounts_id>
|가계부 내역 수정| PATCH| account-books/<int: book_id>/accounts/<int: accounts_id>
|가계부 내역 삭제,취소| PATCH| account-books/<int: book_id>/accounts/<int: accounts_id>/togle_delete
|카테고리 작성| POST| account_category
|카테고리 리스트| GET| account_category
|카테고리 수정| PATCH| account_category/<int: account_category_id>
|카테고리 내역 삭제,취소| PATCH| account_category/toggle_delete/<int: account_category_id>
<br>

## 💾ERD
<br>

<img width="810" alt="ERD" src="https://user-images.githubusercontent.com/57892199/177947917-24549264-1d5e-472a-80f8-1dc621d00e6f.png">
<br>

## 👋 Team & Task
<br>

|Name|Task|
|-----|----
|김동규| 회원가입, 배포
|남효정| 가계부 상세 CRUD
|이동연| 카테고리 CRUD
|전기원| 가계부 CRUD
|조병민| 로그인,로그아웃, JWT
