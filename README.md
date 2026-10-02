# Job Scraper

**여러 채용 사이트를 키워드 하나로 한 번에 훑어 CSV로 내려받는 웹 스크래퍼**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](#기술-스택)
[![Flask](https://img.shields.io/badge/Flask-web%20UI-000000?logo=flask&logoColor=white)](#기술-스택)
[![Scraping](https://img.shields.io/badge/BeautifulSoup%20%2B%20Playwright-static%20%2B%20dynamic-orange)](#설계-판단)

채용 공고는 사이트마다 흩어져 있고 검색 결과 형식도 제각각입니다.
키워드를 한 번 입력하면 **여러 사이트를 차례로 훑어 하나의 목록으로 합치고, CSV로 내보냅니다.**

---

## 주요 기능

- 키워드 하나로 **여러 채용 사이트를 한 번에 수집** (웹 앱에는 BerlinStartupJobs·WeWorkRemotely 2곳이 연결돼 있습니다)
- 사이트마다 다른 결과를 **공통 형식(회사·직무·링크)으로 정규화**해 한 목록으로 병합
- 수집 결과를 화면에서 확인하고 **CSV로 내려받기**
- 같은 키워드 재검색 시 **메모리에 보관한 결과를 재사용**해 불필요한 재수집 차단

## 설계 판단

### 페이지가 만들어지는 방식에 따라 도구를 나눴다

HTML이 서버에서 완성되어 오는 사이트는 `requests` + **BeautifulSoup**으로 충분합니다.
하지만 원티드처럼 **스크롤해야 목록이 더 불러와지는 페이지**는 응답 HTML에 결과가 거의 없습니다.

그래서 원티드용 스크래퍼(`scraper/wanted_scraper.py`)는 **Playwright**로 실제 브라우저를 띄우고
**End 키 입력과 대기를 반복해 무한 스크롤을 재현한 뒤** 렌더링이 끝난 DOM을 읽습니다.
같은 문제를 정적 파싱으로 풀려다 실패하고 도구를 바꾼 경우이고,
**필요한 페이지에만 브라우저를 띄우는 것**이 기준이었습니다.

### 사이트별 스크래퍼를 클래스로 분리했다

`scraper/` 아래에 사이트별 모듈을 두고 같은 인터페이스(수집 → 결과 반환)로 맞췄습니다.
사이트가 하나 늘어도 기존 코드를 고치지 않고 모듈을 추가하면 되고,
**한 사이트의 구조가 바뀌어도 나머지 수집은 계속 동작**합니다.

### 같은 키워드는 다시 긁지 않는다

스크래핑은 느리고 대상 서버에도 부담입니다.
검색 결과를 키워드 단위로 보관해 **같은 요청이 반복될 때 재수집하지 않습니다.**

### User-Agent를 명시했다

기본 요청 헤더로는 차단되거나 다른 페이지가 오는 사이트가 있어, 브라우저와 동일한 User-Agent를 붙여 요청합니다.

## 기술 스택

| 영역 | 기술 |
|---|---|
| 언어 | Python 3.12 |
| 웹 | Flask, Jinja2 템플릿 |
| 수집 | requests + BeautifulSoup (정적 페이지), Playwright (무한 스크롤 페이지) |
| 출력 | CSV 내보내기 |

## 프로젝트 구조

```text
main.py                 Flask 라우팅 (검색·내보내기)
my_file_utils.py        CSV 저장
scraper/                사이트별 스크래퍼 모듈
templates/              검색 화면과 결과 화면
```

## 실행

```bash
pip install flask beautifulsoup4 requests playwright && playwright install
```

```bash
python main.py
```

브라우저에서 `http://localhost:5000` 접속 → 키워드 검색 → CSV 내보내기

## 만든 사람

**Jigwan Joe** — Backend · Data

- GitHub: [@jgjoe](https://github.com/jgjoe)
- Email: jigwan.joe@gmail.com
