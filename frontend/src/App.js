// 리액트의 기능을 사용하기위해 가져와 
import logo from './logo.svg';
import './App.css';
import Device from './Device';
import Mytest from './Mytest';
import axios from 'axios';
import React, { Component } from 'react';
// 이러한 데이터형을 검사할 땐 prop-types를 사용합니다.
// 우선 prop-types를 설치합니다.
import PropTypes from 'prop-types';


// function을 사용하여 함수같지만 이것은 컴포넌트입니다...
/*

컴포넌트를 생성 할 때는 다음과 같이 합니다.
function 컴포넌트명() {
    return (
        반환할 JSX -> JSX????
        javascript를 확장한 문법이라고 한다! (X는 Extend 의 약자일까..?했는데 Javascript XML 이라고 한다ㅎ..)
    );
}
*/



// function App() {

//   {/* jsx에서는 이게 주석이다*/}
//   return (
//     <div className="App">
//       <header className="App-header">
      
//       <img src={logo} className="App-logo" alt="logo" />
//       <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//       {/* <Device /> */}
//       <Mytest />
//       {/* 컴포넌트에 데이터 전달하기  */}
//       {/* 인자를 여러개 보내는 법은 이렇게  */}
//       {/* <Device mydevice="iPad Pro" myfavoritecharacter="Mickey Mouse" /> */}
//       {/* <Device mydevice="Apple Watch" /> */}
//       {/* <Device mydevice="MacBook Pro" /> */}
//       {/* <Device mydevice="AirPods Pro" /> */}
//       {/* 부울변수 전달은 이렇게  */}
//       {/* <Device mydevice="Apple Watch" myfavoritecharacter="Pooh" tf={true} /> */}
//       {/* 숫자를 전달해봅시다 */}
//       {/* <Device mydevice="iPad Pro" myfavoritecharacter="Mickey Mouse" mynum={1} /> */}
//       </header>
//     </div>
//   );

//     // return <div>Hello</div>; 이렇게 한줄로 표현하면 리턴에는 괄호를 제거해도된다. 
// }
 
// // App 컴포넌트 파일에서는 다음의 코드(export)가 있기 때문에 다른 파일에서도 import 할 수 있습니다.
// export default App;



// 이제까지는 실습 편의성을 위해 이렇게 작성한거고, 이제부터는 APP에서 axios를 통해 데이터를 읽어들이자. 

class App extends Component {
  constructor(props) {
      super(props);
      console.log('in constructor');
  }

  state = {
      data : [],
  };
  // (1) App.js파일에서 getMyDeviceData()함수를 실행하여 axios함수를 통해 데이터를 가져옵니다.
  getDeviceData = async () => {
      const {
          data : { myDeviceData },
      } = await axios.get('https://www.everdevel.com/ReactJS/output-axios-data/jsonKey/');

      console.log('data is ' + JSON.stringify(myDeviceData));
      this.setState({data : myDeviceData});
  };

  // componentDidMount() {
  //     console.log('in componentDidMount');
  //     this.getDeviceData();
  // }

  // componentDidUpdate() {
  //     console.log('in componentDidUpdate');
  // }

  // componentWillUnmount() {
  //     console.log('in componentWillUnmount');
  // }
// render는 뭔갈 보여주고자할때 사용하는놈임 
  render() {
      return (
          <div className="App">
            <header className="App-header">
              <img src={logo} className="App-logo" alt="logo" />
              {/* <p>
                  Edit <code>src/App.js</code> and save to reload.
              </p> */}
              <Mytest />
            </header>
          </div>
      )
    
  }

}

export default App;