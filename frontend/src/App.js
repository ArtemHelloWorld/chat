import React, { useState }  from 'react'
import 'bootstrap/dist/css/bootstrap.css';

import ChatList from './components/ChatList';
import PageChats from './components/PageChats';
import useAxios from './utils/useAxios';

async function fetchUserData(username) {
  const api = useAxios();
  let response = await api.get(`api/v1/user_data/${username}/`);
    if (response.status === 200){
      return response.data;
    }
}


function App() {
  const [selectedChat, setSelectedChat] = useState(null);

  if (!selectedChat && window.location.hash){
    let username = window.location.hash.replace('#', '');
    fetchUserData(username).then(chat => setSelectedChat(chat))
  }

  return(
    <div className="container-fluid h-100">
        <div className="row h-100">
            <div className="col-md-3 h-100 overflow-auto p-0">
              <ChatList setSelectedChat={setSelectedChat}/>
            </div>
            <div className="col-md-9 h-100 d-flex flex-column p-0">
              <PageChats selectedChat={selectedChat}/>
            </div>
        </div>
    </div>
  );  
}

export default App;
