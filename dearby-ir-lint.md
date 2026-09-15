# IR HTML 검사

HTML을 수정한 뒤 다음 명령을 실행합니다. 실행 위치와 관계없이 이 자료만 검사합니다.

```sh
rtk proxy node /Users/jominjun/Documents/dearby-ir-lint.mjs
```

다른 컴퓨터에서는 압축을 풀고 해당 폴더에서 `node dearby-ir-lint.mjs`를 실행합니다.
Node.js와 npm이 필요하며 첫 실행 시 HTMLHint 1.9.2를 다운로드합니다.
HTML을 열어 발표할 때는 Node.js나 인터넷이 필요하지 않습니다.

- 검사: 태그 짝, 중복 ID·속성, 따옴표, doctype, 제목, 이미지 alt, 빈 src, 특수문자.
- SVG의 표준 `viewBox` 속성은 대소문자를 유지합니다.
- 오류가 있으면 종료 코드가 0이 아니므로 자동 검사에도 사용할 수 있습니다.
- 저장 시 자동 실행은 설정하지 않았습니다. 편집 후 위 명령으로 검사합니다.
- HTML 린트는 CSS·JavaScript 린트나 화면 검증을 대신하지 않습니다.
  슬라이드 배치, 모바일·인쇄 넘침, 키보드 이동과 캡처 확대는 브라우저에서 별도로 확인합니다.

도구 및 설정 형식: [HTMLHint 공식 문서](https://github.com/htmlhint/HTMLHint#-configuration).
