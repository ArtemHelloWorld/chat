import React, { useState } from 'react';
import useAxios from '../../utils/useAxios';

import LeftPanel from './leftPanel/LeftPanel.jsx';
import ChatList from './ChatList.jsx';
import ChatRoom from './ChatRoom.jsx';

async function fetchChat(username) {
    const api = useAxios();
    let response = await api.get(`api/v1/chat/user/${username}/`);
      if (response.status === 200){
        return response.data;
      }
  }

  
const ChatPage = () => {
    const [selectedChat, setSelectedChat] = useState(null);

    if (!selectedChat && window.location.hash){
        let username = window.location.hash.replace('#', '');
        fetchChat(username).then(chat => setSelectedChat(chat))
    }


    return (
        <div className="container-fluid h-100">
            <div className="row h-100">
                <div className="col-md-3 black-light-bg h-100 d-flex flex-column p-0">
                    <LeftPanel selectedChat={selectedChat} setSelectedChat={setSelectedChat}/>
                </div>
                <div className="col-md-9 black-dark-bg h-100 d-flex flex-column p-0">
                    <ChatRoom selectedChat={selectedChat}/>
                </div>
            </div>
        </div>
    );
}

export default ChatPage;

