# 크롤러

네이트 판의 '사는 얘기'와 루리웹의 '잡담' 게시판의 글 내용을 받아와서 문장 단위로 짜른 후에 오타를 수정해줍니다.

그리고 이를 csv파일의 content column에 저장하고, label은 Nan으로 비워둡니다.

    create_csv(drop_len=2, path='data.csv', page_num=3)
  
문장의 길이가 drop_len 미만일 경우에는 그 문장을 버립니다. path는 저장할 경로, page_num은 크롤링할 페이지의 수입니다. 크면 클수록 데이터는 많아지지만, 느려집니다.
