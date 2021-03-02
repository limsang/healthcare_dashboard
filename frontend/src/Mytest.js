import React, { Component, useState, useEffect  } from 'react';
import axios from 'axios';
import './Mytest.css';
import { useAsync } from 'react-async';
import ScreenImage from './image/screen.png';
import { string } from 'prop-types';
class Mytest extends Component {

    constructor(props) {
        super(props);
        this.host = 'http://127.0.0.1';
        this.port_elasticsearch = '8000';
        this.port_kibana = '5601';
        // this.crud_mode =["인덱스 생성", "인덱스 삭제", "인덱스 목록"]
        
        console.log('in constructor');
    }
 
    // 동적변수를 생성한다. 초기값은 0, 버튼을 누를때마다 값이 변한다. 동적데이터를 다룰려면 state를 사용합니다.
    // 우리가 사용할 axios에서 받아온 데이터도 state에 의해 관리하게합니다
    state = {
        myAge : 0,
        id : "",
        url:"apmall",
        elk_index_nm:"",
        response_state:"",
        select_value: "",
        type_index:["인덱스 생성", "인덱스 삭제", "인덱스 조회"]
    };

    // 액션함수 생성
    plus = () => {
        //  this.setState는 state의 값을 설정할 때 사용합니다. stateValue는 현재의 state를 의미합니다. 
        // stateValue대신 여러분이 원하는 값을 사용할 수 있습니다.
        // 즉, this.setState()함수 안에서 state를 stateValue라는 변수로 사용하겠다는 의미입니다.
        this.setState(stateValue => ({
     
            myAge: stateValue.myAge + 1,
     
            })
        );
    }
 
    minus = () => {
        // console.log('in minus');
        this.setState(stateValue => ({
     
            myAge: stateValue.myAge - 1,
     
            })
        );
    }

    elasticsearch_crud = async () =>{
        var select_option = this.state.select_value;
        var test = document.getElementsByClassName("elkModeSelect");
        var indexNo = test[0].selectedIndex;
        var URL = null;
        switch ( indexNo )
            {
                case 1 :     //변수 = 상수1 이면, 실행문 A 실행
                    URL = this.host + ":" + this.port_elasticsearch + "/" + this.state.url + "/" + 
                    "create_index" + "/" + this.state.elk_index_nm;
                    break;     //swtich { } 코드 블록 탈출
                
                case 2 :     //변수 != 상수1 이고, 변수 = 상수2 이면, 실행문 B 실행
                    URL = this.host + ":" + this.port_elasticsearch + "/" + this.state.url + "/" + 
                    "delete_index" + "/" + this.state.elk_index_nm;
                    break;     //swtich { } 코드 블록 탈출

                case 3 :     //변수 != 상수1 이고, 변수 = 상수2 이면, 실행문 B 실행
                    console.log("indexNo:", indexNo);
                    break;     //swtich { } 코드 블록 탈출

                default :    //변수 != 상수1 이고, 변수 != 상수2 이면, 실행문 C 실행
                    console.log("indexNo:", indexNo);
                    URL = this.host + ":" + this.port_elasticsearch + "/" + this.state.url;

            }
     
        console.log("requesting api:", URL);
        if( !select_option ){ console.log("mode select"); }
        
        console.log('입력받은 select_option:' + select_option);
        const data = await axios.get(URL).then(response => { 
            this.setState(stateValue => ({
                response_state: response.data.state
                })
            );
            console.log(typeof(response), response.data.state);
         })
         .catch(error => {
            if (error.response) {
              // 요청이 이루어졌으며 서버가 2xx의 범위를 벗어나는 상태 코드로 응답했습니다.
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
            else if (error.request) {
              // 요청이 이루어 졌으나 응답을 받지 못했습니다.
              // `error.request`는 브라우저의 XMLHttpRequest 인스턴스 또는
              // Node.js의 http.ClientRequest 인스턴스입니다.
              console.log(error.request);
            }
            else {
              // 오류를 발생시킨 요청을 설정하는 중에 문제가 발생했습니다.
              console.log(error.message);
            }
            console.log(error.config);
            console.log(error.response.data);
            console.log(error.response.status);
            this.setState(stateValue => ({
                response_state: error.response.status
                }));
          });

    }

    appChange = (e) => {
        this.setState({
          id: e.target.value
        });
      }

    urlChange = (e) => {
    this.setState({
        elk_index_nm: e.target.value
    });
    }

    appClick = () => {
    console.log(`id는:${this.state.id}`);
    }
    
    handleChange = (e) => {
        this.setState({select_value: e.target.value});
    }

    render(){
        const { myAge, id, elk_index_nm } = this.state;
        // const { appChange, appClick } = this;
        return(
            <div>
                <header>ELK CRUD API</header>

                <img src = {ScreenImage} width="1000" height="200"></img>
                <br />
                --elk manipulating--
                <br />
              
                {/* 버튼클릭에 대한 액션을 선언해준다. */}
                --sample actions--
                <br />
                <input type="button" value="plus" onClick={this.plus}></input>
                <input type="button" value="minus" onClick={this.minus}></input>
                <br />

                --url test--
                <br />
                <select  className="elkModeSelect" value={this.state.select_value} onChange={this.handleChange}>
                    <option>choose mode</option>
                    <option defaultValue="인덱스 생성">인덱스 생성</option>
                    <option value="인덱스 삭제">인덱스 삭제</option>
                    <option value="인덱스 리스트">인덱스 리스트</option>
                </select>

                <br />
                <input type="text" placeholder="URL" value={elk_index_nm} onChange={this.urlChange} />
                <input type="button" value="API 테스트" onClick={this.elasticsearch_crud}></input>
                <br />
                
                <p>My Age is : { this.state.myAge }</p>
                <p>응답상태 : { this.state.response_state }</p>
                <p>선택된 select 항목 : { this.state.select_value }</p>
              
                <a href="http://127.0.0.1:8000/">확인을 원해??</a> 
                
            </div>
        );
    }

    /* 
    우리는 plus, minus 버튼을 눌러가면서 우리의 나이를 수정했습니다.
    즉, 이것은 정보가 업데이트 된것입니다. 그럼 업데이트 되었기 때문에 componentDidUpdate()가 작동해야합니다.
    하지만 앞에서 우리는 componentDidUpdate()를 선언하지 않았죠.
    해봅시다.
    */

//    componentDidUpdate() {
//     alert('정보가 업데이트되었습니다.');
//     }
}
 
export default Mytest;