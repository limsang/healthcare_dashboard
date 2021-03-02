import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

// App은 컴포넌트의 이름입니다. App 컴포넌트는 여기서 불러옵니다. 위의 코드를 해석하자면 App파일에 있는 App 컴포넌트를 가져온다 입니다.
// ./는 현재 폴더를 의미
import App from './App';

import reportWebVitals from './reportWebVitals';

// render()는 화면에 출력할 때 사용하며 App은 컴포넌트입니다.
// ReactDom.render()은 화면에 내용을 출력하는 기능을 합니다.
// 첫번째 인자인 <App />는 App 컴포넌트가 반환한 내용을 뜻합니다.
// 두번째 인자인 document.getElementById('root')는 App컴포넌트가 반환한 내용이 들어갈 태그입니다. ??
// 즉 id가 root인 태그에 들어갑니다... 태그가 뭐야?

// 컴포넌트를 출력할 때 최종적으로 하나의 태그로만 구성되어야합니다. (여러 컴포넌트를 출력하고싶으면?)
// ReactDOM.render(<div><App /><Device /></div>, document.getElementById('root'));

//혹은...  APP 컴포넌트에 Device 컴포넌트를 넣어버린다. 
ReactDOM.render(<App />,document.getElementById('root'));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
