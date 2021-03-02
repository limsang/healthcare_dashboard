import logo from './logo.svg';
import './App.css';

// 이게 APP 컴포넌트다... 컴포넌트가 뭔지 모르지만 function 키워드가 붙네, App이란 컴포넌트가 있고 
// index.js에 import되고 
// index.js에서 app 컴포넌트를 index.html파일에 있는 id="root"에 뿌린다. 뭐 이정도;;;
function App() {
  return (
    <div className="App">
      
      <header className="App-header">
        
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
