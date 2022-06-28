import { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';


function App() {
	const [zweets, setZweets] = useState([]);
	
	useEffect(()=>{
		function myCallback(reponse, status) {
			if (status === 200) {
				setZweets(reponse);
			} else {
				alert("There was an error.");
			}
		}
		loadTweets(myCallback);
	}, []);

	return (
		<div className="App">
		<header className="App-header">
			<img src={logo} className="App-logo" alt="logo" />
			<p>
				Edit <code>src/App.js</code> and save to reload.
			</p>
			<p>
				{zweets.map((zweet, index)=><li>{zweet.content}</li>)}
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

function loadTweets(callback) {
	const xhr = new XMLHttpRequest();
	const method = 'GET';
	const url = 'http://localhost:8000/api/tweets';
	const responseType = 'json';

	xhr.responseType = responseType;
	xhr.open(method, url);
	xhr.onload = function() {
		callback(xhr.response, xhr.status);
	}
	xhr.onerror = function(e) {
		console.log(e);
		callback({"message": "The request was an error."}, 400);
	}
	xhr.send();
}

export default App;
