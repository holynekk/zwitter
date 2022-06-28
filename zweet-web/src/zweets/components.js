import { useEffect, useState } from 'react';
import { loadTweets } from "../lookup"

export function Zweet(props) {
	const {zweet} = props;
	const className = props.className ? props.className : 'col-10 mx-auto col-md-6';
	return <div className={className}>
		<p>{zweet.id} - {zweet.content}</p>
		<div className='btn btn-group'>
			<ActionButton zweet={zweet} action={{type: "like", display: "Likes"}}/>
            <ActionButton zweet={zweet} action={{type: "like", display: "Unlike"}}/>
            <ActionButton zweet={zweet} action={{type: "retweet", display: "Retweet"}}/>
		</div>
	</div>;
}

export function ActionButton(props) {
	const {zweet, action} = props;
	const className = props.className ? props.className : 'btn btn-primary btn-sm';
    const actionDisplay = action.display ? action.display : 'Action';
    const display = action.type === 'like' ? `${zweet.likes} ${actionDisplay}` : `${actionDisplay}`;
    const handleClick = (event) => {
        event.preventDefault();
        if (action.type === 'like') {
            
        }
    };
	return <button className={className}> {display} </button>
}

export function ZweetList(props) {
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
	return zweets.map((item, index)=><Zweet zweet={item} className='my-5 py-5 border bg-white text-dark' key={index}/>);
}
