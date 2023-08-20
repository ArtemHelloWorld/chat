import React, { useState, useEffect, useRef, useContext }  from 'react'
import { scrollToElement } from '../../utils/ScrollDown';
import AuthContext from '../../context/AuthContext';
import useAxios from '../../utils/useAxios';
import ChatRoomMessage from './ChatRoomMessage.jsx';



function PageChats({ selectedChat }) {
  const chatSocket = useRef();
  const [connected, setConnected] = useState(false);

  const [isTyping, setIsTyping] = useState(false);
  const [isCompanionTyping, setIsCompanionTyping] = useState(false);

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
    return new WebSocket(url);
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
      else if (data.type === 'user_typing'){
        if (data.sender === selectedChat.id){
            //setTimeout(() => {setIsCompanionTyping(false);}, 2000)
            setIsCompanionTyping(data.typing);
        }
      }
      else if (data.type === 'mark_message_as_read'){
        console.log(data.message_pk, 'dd')
        setChatMessages(prev => [...prev.map(message => message.id===data.message_pk ? {...message, is_read: true}: {...message})])
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

  const sendTypingStatus = async () => {
    if (connected){
      chatSocket.current.send(JSON.stringify({
        'typing': isTyping,
      }))
    }
  }

  const sendMessageInput = async () => {
    if(connected && messageInput !== ''){
      chatSocket.current.send(JSON.stringify({
        'message': messageInput,
      }))
      setMessageInput('')
    }
  }
  const markMessageAsRead = async (message) => {
    if(connected){
      chatSocket.current.send(JSON.stringify({
            'mark_message_as_read': message.id,
        }))
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
      scrollToElement('.messages', 'li.unread');
    }
  }, [connected]);


  useEffect(() => {
    sendTypingStatus();
  }, [isTyping])


  if (selectedChat && connected){
    return(
      <>
        <div className="header py-3">
          <div className="container ">
            <h1 className="mb-0">{selectedChat.username}</h1>
            {isCompanionTyping && <small>Печатает...</small>}
          </div>
        </div>

        <div className="messages flex-grow-1 overflow-auto mb-3 px-5">
          <ul className="message-list list-unstyled d-flex flex-column gap-2 my-3 px-5">
            {chatMessages.map((message) => (
              <ChatRoomMessage
                message={message}
                onMessageRead={markMessageAsRead}
                position={message.sender === user.user_id ? 'right': 'left'}
              />
            ))}
          </ul>
        </div>

        <div className="container">
          <div id="message-form" className="input-group input-group-lg mx-auto mb-3 justify-content-end w-50" >
            <input
              id="message-input"
              type="text"
              className="form-control rounded-pill rounded-end"
              placeholder="Cообщение..."
              value={messageInput}
              onChange={event => {setMessageInput(event.target.value); setIsTyping(true); console.log('typing...')}}
              onBlur={event => {setIsTyping(false); console.log('not typing')}}
              onKeyDown={(event) => {event.key === 'Enter' && sendMessageInput()}}
              >
            </input>
            <button onClick={sendMessageInput} className="btn btn-primary rounded-pill rounded-start">Отправить</button>
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