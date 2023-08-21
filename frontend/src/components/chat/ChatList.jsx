import React, {useState, useEffect, useContext} from 'react'
import useAxios from '../../utils/useAxios';
import authContext from '../../context/AuthContext.js';
import ReconnectingEventSource from "reconnecting-eventsource";

export default function ChatList({ setSelectedChat }){

  const [chats, setChats] = useState([]);
  const {user, accessToken} = useContext(authContext);
  const api = useAxios();



  async function fetchChats() {
    let response = await api.get('api/v1/chat/all/');
    if (response.status === 200){
      console.log(response.data)
      setChats(response.data)
    }
  }

  useEffect(() => {
    console.log('ФЕТЧИМ ЧАТЫ')
    fetchChats()


    const eventSource = new ReconnectingEventSource(`http://127.0.0.1:8000/api/v1/chat/notifications/${user.user_id}/${accessToken}/events/`);
    eventSource.onopen = () => {
      console.log('eventSource open', eventSource)

    }
    eventSource.onmessage = (event) => {
       const data = JSON.parse(event.data);
       console.log('eventSource message:', data);
       if ('last_message' in data){
         setChats(prev => [...prev.map(chat => chat.id === data.id ? {...chat, last_message: `${data.last_message}`} : {...chat})])
       }
       else if ('status' in data){
         // todo: проверить, что печатаешь не ты
         setChats(prev => [...prev.map(chat => chat.id === data.id ? {...chat, status: data.status} : {...chat})])
       }
    };
    eventSource.onerror = () => {
       console.log('eventSource error');
       eventSource.close();
    }
     eventSource.addEventListener('stream-error', function (e) {
          eventSource.close();
        }, false);
     eventSource.addEventListener('keep-alive', function (e) {
          console.log(e, 'stream-reset')
        }, false);
  }, []);



  const handleChatClick = (chat) => {
    setSelectedChat(chat);
  };


  return (
    <ul id="users" className="list-group my-3">
      {chats.map((chat) => (
        <li key={chat.id} onClick={() => handleChatClick(chat)} className='mb-1'>
          <a href={`#${chat.companion.username}`} className="card d-flex flex-row align-items-center text-decoration-none p-3">
            <img src="user1.jpg" alt="" className="user-photo me-3" />
            <div className="user-info">
              <h4 className="user-username">{chat.companion.username}</h4>
              <p className="user-description">{chat.status!==null ? chat.status : chat.last_message}</p>
            </div>
          </a>
        </li>
      ))}
    </ul>
  );
}