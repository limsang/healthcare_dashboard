import React from 'react';
import PropTypes from 'prop-types';
// Device.js는 App으로부터 전달받은 porps를 활용하여 JSX코드를 반환합니다.
function Device( {name, ram, homeButton, touchID, faceID, cpu} ) {
    // JSX안에서는 제어문을 사용할 수 없어서 삼항연산자를 사용했는데요. 
    // 이번엔 HomeButton은 원래대로 변경하고 if문을 사용해서 값을 출력할 값을 변경하도록 하겠습니다.
    if (homeButton == true) {
        homeButton = "있음";
    }else {
        homeButton = "없음";
    }
    return (
        <div>

            <p>
                Edit <code>src/App.js</code> and save to reload.
            </p>
            <h3>Name : {name}</h3>
            <h3>RAM : {ram}</h3>
            {/* JSX안에서는 제어문을 사용할 수 없습니다. 하지만 삼항연산자는 사용할 수 있습니다.  */}
            {/* <h3>Home Button : { homeButton == true ? "있음" : "없음" }</h3> */}
            <h3>Home Button : { homeButton }</h3>
            <h3>TouchID : {touchID}</h3>
            <h3>FaceID : {faceID}</h3>
            {/* CPU 에 대한 정보는 없어,,, 디폴트값을 전달해줘야해. */}
            <h3>CPU : {cpu}</h3>
        </div>
    );

    
}




/* 
prop types 적용방법.. 이거 왜한다고? -> 데이터의 데이터형을 검사하려면 prop-types를 사용합니다.
 우리가 Device컴포넌트에서 사용하는 데이터는 다음과 같음

 [
    {
        "key":1,
        "name":"iPad Pro",
        "RAM":6,
        "HomeButton":false,
        "TouchID":"No",
        "FaceID":"Yes"
    }
]

컴포넌트명.propTypes = {
    props명: PropTypes.데이터형.필수여부
};


*/
Device.propTypes = {
    name: PropTypes.string.isRequired,
    ram: PropTypes.number.isRequired,
    homeButton: PropTypes.bool.isRequired,
    touchID: PropTypes.string,
    faceID: PropTypes.string,
};
 

// 값이 없을 때 어떻게 기본값을 설정하는 방법에 대해 알아봅시다.
// defaultProps 사용하기, cpu에 대한 정보가 없다고 가정하자
Device.defaultProps = {
    cpu : "cpu정보가 없습니다.",
};

export default Device;