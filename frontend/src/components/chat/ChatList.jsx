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
      return response.data
    }
  }
  async function getMessageInfo(message_id) {
    if (message_id) {
      let response = await api.get(`api/v1/message/${message_id}/`);
      if (response.status === 200) {
        return response.data
      }
    }
    return null
  }


  useEffect(() => {
    console.log('ФЕТЧИМ ЧАТЫ')
    fetchChats().then(chats => {
        setChats(chats)
      }
    )


    const eventSource = new ReconnectingEventSource(`http://127.0.0.1:8000/api/v1/chat/notifications/${user.user_id}/${accessToken}/events/`);
    eventSource.onopen = () => {
      console.log('eventSource open', eventSource)

    }
    eventSource.onmessage = (event) => {
       const data = JSON.parse(event.data);
       console.log('eventSource message:', data);
       if ('last_message_info' in data){
         setChats(prev => [...prev.map(chat => chat.id === data.id ? {...chat, last_message_info: data.last_message_info} : {...chat})])
       }
       else if ('status' in data){
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

  const getChatDescription = (chat) => {
    for (var active_user in chat.status){
      if (chat.status.hasOwnProperty(active_user) && active_user.toString() !== user.user_id.toString()){
        if (chat.status[active_user]){
          return chat.status[active_user]
        }
      }
    }
    if(chat.last_message_info){
      return chat.last_message_info.text
    }
    else {
      return ''
    }
  }
  const handleChatClick = (chat) => {
    setSelectedChat(chat);
  };

  if(chats) {
    return (
        <ul id="users" className="list-group my-3">
          {chats.map((chat) => (
            <li key={chat.id} onClick={() => handleChatClick(chat)} className='mb-1' style={{ listStyle: 'none' }}>
              <a href={`#${chat.companion.username}`} className="card text-decoration-none d-block h-100 p-0">
                <div className="row align-items-start h-100">
                  <div className="col-md-4">
                    <div className="card-img-square">
                      {chat.companion.profile_image && (
                        <img
                          src={
                            chat.companion.profile_image.indexOf('http') === -1
                              ? 'http://127.0.0.1:8000' + chat.companion.profile_image
                              : chat.companion.profile_image
                          }
                          alt=""
                          className="img-fluid"
                          style={{ height: '5rem', width: 'auto' }}
                        />
                        )
                      }
                    </div>
                  </div>
                  <div className="col-md-8 d-flex flex-column">
                    <div className="d-flex flex-column h-100">
                      <h4 className="user-username overflow-hidden text-truncate align-self-start">{chat.companion.username}</h4>
                      <p className="user-description overflow-hidden text-truncate align-self-start">
                        {getChatDescription(chat)}
                      </p>
                    </div>
                  </div>
                </div>
              </a>
            </li>
          ))}
        </ul>
    );
  }
  else{
    return (
        <></>
    )
  }
}