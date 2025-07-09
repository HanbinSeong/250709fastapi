# 게시판(board) 기능사항 정의서
    - 목록화면
        - 목록: 번호, 제목, 작성자, 작성일, 조회수, 좋아요
        - 제목 클릭시 상세화면 이동
        - 글쓰기 버튼 클릭시 작성화면 이동
    - 수정화면
        - 제목, 내용
        - 저장, 취소
    - 작성화면
        - 제목, 작성자, 내용
        - 버튼: 취소, 등록
    - 상세화면
        - 좋아요 표시, 조회수 표시, 제목, 내용
        - 버튼: 수정버튼 클릭시 수정화면, 삭제버튼

## DB 스키마 정의
    - 게시글 테이블
        ```
            `id`     INT            NOT NULL PRIMARY KEY,
            `title`  VARCHAR(255)   NOT NULL,
            `author` VARCHAR(100)   NOT NULL,
            `date`   DATE           NOT NULL DEFAULT Datetime.now,
            `views`  INT            NOT NULL DEFAULT 0,
            `like`   INT            NOT NULL DEFAULT 0,
            `content` TEXT          NOT NULL
        ```

## API 정의
    - 목록화면
        - 목록조회(GET)
    - 상세화면
        - 조회수 증가
        - 좋아요 증가
        - 좋아요 기능
        - 삭제 기능
    - 수정화면
        - 저장기능
    - 작성화면
        - 등록기능 (제목, 작성자, 내용만 기입)

# TODO LIST
    - 메인 화면
        - 추가버튼 (Create) - Post
        - 완료 체크버튼 (True, False) - Post
        - 삭제 버튼 (Delete) - Post
    