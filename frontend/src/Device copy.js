// import React from 'react';

// 이렇게 받아오면 React.Component 클래스를 상속 받을 때 React.를 작성하지 않아도 괜찮습니다.
// React 컴포넌트 클래스를 상속받았기 때문에 우리는 render() 메서드, JSX, this.state등의 다양한 메서드를 사용할 수 있게 되었습니다.
import React, { useState, useEffect, Component } from 'react';
import axios from 'axios';


// function Device({ mydevice, myfavoritecharacter }) {
    
//     console.log(JSON.stringify(myfavoritecharacter));
 
//     return <div>My { mydevice }, { myfavoritecharacter }</div>;
// }

const mydata = {
    "myDeviceData":[
      {
        "name":"iPad Pro",
        "RAM":6,
        "HomeButton":false,
        "TouchID":"No",
        "FaceID":"Yes"
      },{
        "name":"iPhone Xs",
        "RAM":4,
        "HomeButton":false,
        "TouchID":"No",
        "FaceID":"Yes"
      },{
        "name":"iPhone 6",
        "RAM":1,
        "HomeButton":true,
        "TouchID":"Yes",
        "FaceID":"No"
      }
    ]
};
//  이건... map함수를 이용해서 for문없이 출력하는법
/*

'데이터'.map(('map()안에서 사용할 데이터의 변수') => {
    document.write('map()안에서 사용할 데이터의 변수' is ' + JSON.stringify('map()안에서 사용할 데이터의 변수'));
});

*/
//  함수형 컴포넌트는 이정도로 마무리하고 클래스형 컴포넌트로 넘어가자..
// function Device(data) {
//     return (
//         <div>
//             {
//                 mydata.myDeviceData.map((myAppleDevice) => {
//                     console.log('idx is ' + JSON.stringify(myAppleDevice.name));
//                     return(
//                         <div>
//                             이름 : { myAppleDevice.name } <br></br>
//                             램 : { myAppleDevice.RAM }GB<br></br>
//                             홈버튼 : { ((myAppleDevice.HomeButton === true) ? '있음' : '없음') } <br></br>
//                             터치 ID : { myAppleDevice.TouchID } <br></br>
//                             페이스 ID : { myAppleDevice.FaceID } <br></br><br></br>
//                          </div>
//                     );
//                 })
//             }
//         </div>
//     );
// }


// function Device(data) {
//     // 데이터를 전달하는 방법 props명="값"
//     // JSON.stringify()는 변수 값, 배열, 객체 등을 문자열로 출력해줍니다.
//     console.log(JSON.stringify(data)); 
//     // const는 상수를 선언 할 때 사용합니다.
//     // JSX에서는 대괄호없이 props를 사용하면 그냥 문자열이므로 props로 인식시키기 위해 대괄호를 사용합니다.


//     // data 대신 이름을 동일하게 해주면 위와 같이 더 간단하게 출력할 수 있습니다.
//     const { mydevice } = data;
//     // return <div>My { mydevice }</div>;
//     return <div>My ???{ mydevice }</div>;

// }



// 우리가 외부에서 데이터를 가져오고 이것을 다룰려면 앞에서 학습했던 컴포넌트 선언방식으로는 무리입니다.
// 자 그럼, Device 컴포넌트를 클래스형 컴포넌트로 변경합시다.

//  클래스는 처음 실행할 때 생성자가 우선 실행되고 마지막으로 소멸자가 실행됩니다.
// render함수외에도 다음의 함수들을 사용할 수 있습니다.

// constructor(), componentDidMount(), componentDidUpdate(), componentWillUnmount()


class Device extends Component {
    // constructor() 함수내에는 필수적으로 super(props); 코드를 넣어줍니다., 생성자임 
    // super는 부모클래스의 생성자를 의미합니다.
    // 부모 클래스라하면 우리가 상속받고 있는 React.Component 클래스를 의미합니다.
    // 그럼 이걸 왜 사용하는가는 super()함수를 호출하지 않으면 this 키워드를 사용할 수 없기 때문입니다.
    // 즉 클래스 안에서는 props를 사용하려면 this키워드로 접근해야하는데 사용할 수 없기때문이죠.
    constructor(props) {
        super(props);
        console.log('in constructor');
    }


    // axios 를 통해 받은 동적 데이터를 관리해보자 
    // 배열을 적용하기때문에 []를 값으로 넣었습니다.
    state = {
        data : [],
    };

    // 데이터를 제대로 받기 위해서는 async와 await 키워드를 사용해야합니다.
    // 데이터가 엄청 초고속으로 들어왔다면 데이터를 받았을수도 있지만 이런 불확실성으로 프로그래밍을 할 순 없습니다.
    // 이것을 사용하려면 함수를 생성할 때 function가 아닌 화살표 함수를 사용하여 함수를 생성합니다.
    // 위와 같이 async는 함수에, await는 axios에 작성합니다.
    
    // getMyData = async () => {

    //     //const대신 let을 사용했습니다. const는 상수이므로 값이 변하지 않기 때문에 다시 값을 대입하려면 사용할 수 없습니다
    //     let data = await axios.get('https://www.everdevel.com/ReactJS/output-axios-data/jsonKey/');

    //     // 우리는 myDeviceData에 접근하기 위해 data변수에 대입해서 data.data.mydevice 이렇게 접근해야했습니다.
    //     data = data.data.myDeviceData;
    //     console.log('data is ' + JSON.stringify(data));
    //     this.setState({data});
    //     // 요렇게 동적변수에 값을 할당할 수 있음
    //     // const data = await axios.get('https://jsonplaceholder.typicode.com/');
    //     // const data = await axios.get('http://127.0.0.1:8000/apmall/');
    //     // const data = await axios.get('http://127.0.0.1:8000/apmall/create_index/reacttest7');
    //     // data = data.data.myDeviceData;
    //     console.log('data is ' + JSON.stringify(data));
    //     // console.log("type is" + data);
    // };

    // 우리는 myDeviceData에 접근하기 위해 data변수에 대입해서 data.data.mydevice 이렇게 접근해야했습니다.
    // 구조분해할당이라는 개념을 활용해서 코드를 드라이하게 만들어보자 (구조 분해 할당은 ReactJS 문법이 아닌 JavaScript의 문법입니다.)
    getMyData = async () => {
        const {
            data : { myDeviceData },
        } = await axios.get('https://www.everdevel.com/ReactJS/output-axios-data/jsonKey/');
 
        console.log('data is ' + JSON.stringify(myDeviceData));
        this.setState({data : myDeviceData});
    };

    componentDidMount() {
        console.log('in componentDidMount');
        this.getMyData();
    }
    // componentDidUpdate()함수는 화면에 어떠한 정보가 업데이트되면 실행됩니다.
    // 아직 우리는 render()함수가 실행 후 화면에 어떠한 정보를 업데이트하지 않기 때문에 componentWillUnmount()가 실행되지 않습니다.
    componentDidUpdate() {
        console.log('in componentDidUpdate');
    }
 
    // 마지막으로 클래스가 종료될 때 소멸자인 componentWillUnmount()가 실행됩니다.
    componentWillUnmount() {
        console.log('in componentWillUnmount');
    }
    
    // map함수안에서 데이터를 전달할 때 return문을 사용함을 잊지마세요.
    //  데이터를 return할 때 key값도 리턴을 해야하기 때문입니다. p태그의 속성에 key속성을 추가하고 key값을 입력해줍니다.
    // 딕셔너리의 키와 비슷한개념인가봄.. 겹치지않는 값들로 구성한다 
    render() {
        return (
            <div>
                {
                this.state.data.map((myDeviceData) => {
                    return <p key={ myDeviceData.key }>name : { myDeviceData.name }</p>;
                })
                }
            </div>
        );
    }


    // render() {
    //     return <div>Here is Device Component</div>;
    // }
}
 



//  외부로부터 또는 데이터베이스에서 데이터를 받아야 하는 경우도 있지요.
// 그러한 경우에는 axios를 사용하여 데이터를 전달받습니다.
// axios를 사용하려면 먼저 axios를 설치해야합니다.
// axios 설치명령어는 npm install axios입니다.
// 데이터의 데이터형을 검사하려면 prop-types를 사용합니다.

export default Device;