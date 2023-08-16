import React, { useState, useEffect, useRef, useContext }  from 'react'
import { scrollDown } from '../utils/ScrollDown';
import AuthContext from '../context/AuthContext';
import useAxios from '../utils/useAxios';




function PageChats({ selectedChat }) {
  const chatSocket = useRef();
  const [connected, setConnected] = useState(false);
  const [messageInput, setMessageInput] = useState('');
  const [chatMessages, setChatMessages] = useState([]);

  const {user, accessToken} = useContext(AuthContext);
  const api = useAxios();



  async function fetchChatId() {
    let response = await api.get(`api/v1/chat/user/${selectedChat.username}/`);
    if (response.status === 200){
      return response.data.id;
    }
  }


  async function fetchMessages() {
    let response = await api.get(`api/v1/chat/user/${selectedChat.username}/messages/`);
    if (response.status === 200){
      return response.data;
    }
  }

  function newWebSocket(chat_id){
    let url = `ws://localhost:8000/ws/socket-server/chat/${accessToken}/${chat_id}/`

    if (chatSocket.current) {
      if (chatSocket.current.url !== url) {
        chatSocket.current.close();
      }
    }
    return new WebSocket(url)
  }

  function loadWebSocket(chat_id){
    chatSocket.current = newWebSocket(chat_id);

    chatSocket.current.onopen = () => {
      setConnected(true);
      console.log('Socket connected');
    }

    chatSocket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if(data.type === 'chat'){
        setChatMessages(prev => [...prev, data])
        console.log('onmessage', event.data)
      }
    }
    chatSocket.current.onclose = (event) => {
      setConnected(false);
      console.log('Socket clost');
    }
    chatSocket.current.onerror = (event) => {
      console.log('Socket error');
    }
  }



  useEffect(() => {
    if (selectedChat){
      console.log('ФЕТЧИМ ЧАТ ID И СОЗДАЕМ WS');
      fetchChatId().then(chat_id => loadWebSocket(chat_id));

      console.log('ФЕТЧИМ СООБЩЕНИЯ', selectedChat);
      fetchMessages().then(messages => setChatMessages(messages));
    }
  }, [selectedChat]);


  useEffect(() => {
    if(chatMessages.length){
      scrollDown('.messages');
    } 
  }, [chatMessages]);




  const sendMessageInput = async () => {
    if(messageInput !== ''){
      chatSocket.current.send(JSON.stringify({
        'message': messageInput,
      }))
      setMessageInput('')
    }
  }


  if (selectedChat){
    return(
    <>
          <h2 className="mt-3">{selectedChat.username}</h2>
          <div className="messages flex-grow-1 overflow-auto mb-3 px-5">
            <ul className="message-list list-unstyled d-flex flex-column gap-2 my-3 px-5">
              {chatMessages.map((message) => (
                <React.Fragment key={message.id}>
                  {message.sender === user.user_id ? (
                    <li className={`message-right px-3 align-self-end w-65 ${message.is_read ? 'read' : ''}`} id={message.id}>
                      <div className="d-flex justify-content-end">
                        <div className="rounded-3 p-2 bg-light text-black text-start" style={{wordBreak: 'break-word'}}>{message.text}
                          <div className="align-self-end"><small className="-flex justify-content-end text-muted">{message.time_sending}</small></div>
                        </div>
                      </div>
                    </li>
                  ) : (
                    <li className={`message-left px-3 align-self-start w-65 ${message.is_read ? 'read' : ''}`} id={message.id}>
                      <div className="d-flex justify-content-start">
                        <div className="rounded-3 p-2 bg-secondary text-light text-start" style={{wordBreak: 'break-word'}}>{message.text}
                          <div className="align-self-end"><small className="message-time d-flex justify-content-end">{message.time_sending}</small></div>
                        </div>
                      </div>
                    </li>
                  )}
                </React.Fragment>
              ))}
            </ul>
          </div>
          <div className="container">
            <div id="message-form" className="input-group input-group-lg mx-auto mb-3 justify-content-end w-50" >
              <input id="message-input" type="text" name="message-input" className="form-control rounded-pill rounded-end" placeholder="Cообщение..." value={messageInput} onChange={e => setMessageInput(e.target.value)} onKeyDown={(event) => {event.key === 'Enter' && sendMessageInput()}}></input>
              <button className="btn btn-primary rounded-pill rounded-start" onClick={sendMessageInput}>Отправить</button>
            </div>
          </div>
        </>
    )
  }
  else{
    return (
      <>
      </>
      )
  }
    
}

export default PageChats;