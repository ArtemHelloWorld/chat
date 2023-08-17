import React, {useState, useEffect} from 'react'
import useAxios from '../../utils/useAxios';

export default function ChatList({ setSelectedChat }){

  const [chats, setChats] = useState([]);
  const api = useAxios();



  async function fetchChats() {
    let response = await api.get('api/v1/users/all/');
    if (response.status === 200){
      setChats(response.data)
    }
  }

  useEffect(() => {
    console.log('ФЕТЧИМ ЧАТЫ')
    fetchChats()
  }, []);



  const handleChatClick = (chat) => {
    setSelectedChat(chat);
  };


  return (
    <ul id="users" className="list-group my-3">

      {chats.map((chat) => (

        <li key={chat.id} onClick={() => handleChatClick(chat)} className='mb-1'>
          <a href={`#${chat.username}`} className="card d-flex flex-row align-items-center text-decoration-none p-3">
            <img src="user1.jpg" alt="" className="user-photo me-3" />
            <div className="user-info">
              <h4 className="user-username">{chat.username}</h4>
              <p className="user-description">Description about {chat.username}</p>
            </div>
          </a>
        </li>
        
      ))}
    </ul>

  );
}